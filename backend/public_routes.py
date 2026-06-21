from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from backend.models import db, Domain, Course, Video, ContactMessage, Enrollment, User, ChatbotConversation
from backend.services.ai.rulebased_chatbot_service import build_rulebased_chatbot_payload
from datetime import datetime
import re
import os
import glob
import unicodedata
from sqlalchemy import or_

public_bp = Blueprint('public', __name__)

COURSE_IMAGE_MAP = {
    "aws": "aws.png",
    "data analytics powerbi": "data_analytics_powerbi.png",
    "deep learning": "deep_learning.jpeg",
    "docker kubernetes": "docker_kubernetes.png",
    "ethical hacking": "ethical_hacking.png",
    "flask fullstack": "flask_fullstack.jpg",
    "flutter": "flutter.png",
    "machine learning": "machine_learning.jpg",
    "mern stack": "mern_stack.jpg",
    "network security": "network_security.jpg",
    "nextjs": "nextjs.jpg",
    "nlp": "nlp.jpg",
    "python data science": "python_for_datascience.jpg",
    "react js": "react_js.png",
    "react native": "react_native.png",
}

DOMAIN_IMAGE_MAP = {
    "Web Development": "https://images.unsplash.com/photo-1498050108023-c5249f4df085",
    "Data Science": "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
    "Artificial Intelligence": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
    "Cyber Security": "https://images.unsplash.com/photo-1510511459019-5dda7724fd87",
    "Cybersecurity": "https://images.unsplash.com/photo-1510511459019-5dda7724fd87",
    "Cloud Computing": "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
    "Mobile Development": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c",
}


def _visible_domains_query():
    return Domain.query.filter(~Domain.name.ilike('qa domain%'))


def _normalize_slug(text):
    text = unicodedata.normalize('NFKD', (text or '')).encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def _course_image_candidates(course):
    """Generate probable file names for a course image in static/images/courses."""
    candidates = []
    title = (course.title or '').strip()
    slug = _normalize_slug(title)
    compact = slug.replace('-', '')
    underscored = slug.replace('-', '_')

    if slug:
        candidates.extend([slug, compact, underscored])

    # Exact mapping for known courses.
    title_key = title.lower()
    for key, mapped_file in COURSE_IMAGE_MAP.items():
        if key in title_key:
            mapped_base = os.path.splitext(mapped_file)[0]
            candidates.extend([mapped_base, mapped_base.replace('_', '-')])

    # Common alias mapping for frequent course names.
    alias_map = {
        "machine learning": ["ml", "machine-learning", "machine_learning"],
        "react js": ["react", "react-js", "react_js"],
        "react": ["react", "react-js", "react_js"],
        "python": ["python", "python-programming", "python_programming"],
        "python data science": ["python_datascience", "python-data-science", "pythondatascience"],
        "data analytics powerbi": ["data_analytics_powerbi", "data-analytics-powerbi", "dataanalyticspowerbi"],
        "power bi": ["data_analytics_powerbi", "powerbi"],
    }
    for key, aliases in alias_map.items():
        if key in title_key:
            candidates.extend(aliases)

    image_url = (course.image_url or '').strip()
    if image_url and not image_url.startswith(('http://', 'https://', '/')):
        image_base = _normalize_slug(os.path.splitext(os.path.basename(image_url))[0])
        if image_base:
            candidates.extend([image_base, image_base.replace('-', '_'), image_base.replace('-', '')])

    # Preserve order and uniqueness.
    deduped = []
    seen = set()
    for candidate in candidates:
        if candidate and candidate not in seen:
            deduped.append(candidate)
            seen.add(candidate)
    return deduped


def _local_image_index():
    """Index local images from static/images recursively."""
    images_root = os.path.join(os.getcwd(), 'static', 'images')
    if not os.path.isdir(images_root):
        return {}

    index = {}
    valid_ext = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    for path in glob.glob(os.path.join(images_root, '**', '*.*'), recursive=True):
        ext = os.path.splitext(path)[1].lower()
        if ext not in valid_ext:
            continue
        key = _normalize_slug(os.path.splitext(os.path.basename(path))[0])
        if not key:
            continue
        rel = os.path.relpath(path, os.path.join(os.getcwd(), 'static')).replace('\\', '/')
        index.setdefault(key, rel)
    return index


def _domain_image_candidates(course):
    domain_name = ((getattr(course, 'domain', None) and course.domain.name) or '').strip()
    if not domain_name:
        return []
    slug = _normalize_slug(domain_name)
    return [slug, slug.replace('-', ''), slug.replace('-', '_')]

def resolve_course_image_url(course):
    """Resolve final public URL for course image using local-first strategy."""

    image_url = (course.image_url or '').strip()
    images_dir = os.path.join(os.getcwd(), 'static', 'images', 'courses')
    local_images = _local_image_index()

    if not os.path.isdir(images_dir):
        domain_name = ((getattr(course, 'domain', None) and course.domain.name) or '').strip()
        if domain_name and domain_name in DOMAIN_IMAGE_MAP:
            return DOMAIN_IMAGE_MAP[domain_name]
        return url_for('static', filename='images/courses/default_course.png')

    try:
        files = os.listdir(images_dir)
    except Exception:
        domain_name = ((getattr(course, 'domain', None) and course.domain.name) or '').strip()
        if domain_name and domain_name in DOMAIN_IMAGE_MAP:
            return DOMAIN_IMAGE_MAP[domain_name]
        return url_for('static', filename='images/courses/default_course.png')

    if image_url.startswith(('http://', 'https://')):
        return image_url

    if image_url:
        exact_file_name = os.path.basename(image_url)
        exact_path = os.path.join(images_dir, exact_file_name)
        if os.path.isfile(exact_path):
            return url_for('static', filename=f'images/courses/{exact_file_name}')

    files_by_name = {}
    for file_name in files:
        name_no_ext = _normalize_slug(os.path.splitext(file_name)[0])
        files_by_name[name_no_ext] = file_name

    candidates = _course_image_candidates(course)
    for candidate in candidates:
        matched = files_by_name.get(_normalize_slug(candidate))
        if matched:
            return url_for('static', filename=f'images/courses/{matched}')

    for candidate in candidates:
        rel = local_images.get(_normalize_slug(candidate))
        if rel:
            return url_for('static', filename=rel)

    for candidate in _domain_image_candidates(course):
        rel = local_images.get(_normalize_slug(candidate))
        if rel:
            return url_for('static', filename=rel)

    domain_name = ((getattr(course, 'domain', None) and course.domain.name) or '').strip()
    if domain_name and domain_name in DOMAIN_IMAGE_MAP:
        return DOMAIN_IMAGE_MAP[domain_name]

    return url_for('static', filename='images/courses/default_course.png')


def attach_course_image_urls(courses):
    for course in courses:
        course.resolved_image_url = resolve_course_image_url(course)
        course.resolved_image = course.resolved_image_url
    return courses


def _visible_courses_query():
    """Public-safe course list: published only and excludes obvious temp/test titles."""
    noise_match = or_(
        Course.title.ilike('%phase2 temp%'),
        Course.title.ilike('%phase2 empty%'),
        Course.title.ilike('stability %'),
        Course.title.ilike('% stability %'),
        Course.title.ilike('temp %'),
        Course.title.ilike('% temp course%'),
        Course.title.ilike('test %'),
        Course.title.ilike('% test course%'),
        Course.title.ilike('qa course%'),
        Course.title.ilike('qa domain%'),
        Course.title.ilike('% qa course %'),
        Course.title.ilike('% qa domain %'),
        Course.domain.has(Domain.name.ilike('qa domain%')),
    )
    return Course.query.filter(Course.status == 'published').filter(~noise_match)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@public_bp.route('/')
def index():
    """Home Page"""
    try:
        # Get statistics for homepage
        total_courses = _visible_courses_query().count()
        total_domains = _visible_domains_query().count()
        total_students = User.query.filter_by(role='student').count()
        total_enrollments = Enrollment.query.count()
        
        # Get featured courses (first 6)
        featured_courses = (
            _visible_courses_query()
            .order_by(Course.created_at.desc())
            .limit(6)
            .all()
        )
        attach_course_image_urls(featured_courses)
        
        return render_template('public/index.html',
                             total_courses=total_courses,
                             total_domains=total_domains,
                             total_students=total_students,
                             total_enrollments=total_enrollments,
                             featured_courses=featured_courses)
    except Exception as e:
        print(f"Error loading home page: {e}")
        flash('Error loading page. Please try again.', 'danger')
        return render_template('public/index.html',
                             total_courses=0,
                             total_domains=0,
                             total_students=0,
                             total_enrollments=0,
                             featured_courses=[])

@public_bp.route('/courses')
def courses():
    """Courses Page (Domain Based)"""
    try:
        # Get all domains with their courses
        domains = _visible_domains_query().all()
        
        # Option to filter by domain
        domain_filter = request.args.get('domain', '')
        search_query = request.args.get('search', '').strip()
        
        query = _visible_courses_query()
        if domain_filter:
            query = query.filter(Course.domain_id == domain_filter)
        if search_query:
            query = query.filter(
                Course.title.ilike(f'%{search_query}%') |
                Course.description.ilike(f'%{search_query}%')
            )
        courses_list = query.order_by(Course.created_at.desc()).all()

        attach_course_image_urls(courses_list)
        
        return render_template('public/courses.html',
                             domains=domains,
                             courses=courses_list,
                             selected_domain=domain_filter,
                             search_query=search_query)
    except Exception as e:
        print(f"Error loading courses page: {e}")
        flash('Error loading courses. Please try again.', 'danger')
        return render_template('public/courses.html',
                             domains=[],
                             courses=[],
                             selected_domain='',
                             search_query='')

@public_bp.route('/course/<int:course_id>')
def course_detail(course_id):
    """Course Detail Page"""
    try:
        course = Course.query.get_or_404(course_id)
        course.resolved_image_url = resolve_course_image_url(course)
        for related_course in course.domain.courses:
            related_course.resolved_image_url = resolve_course_image_url(related_course)
        videos = Video.query.filter_by(course_id=course_id).order_by(Video.order_number).all()
        syllabuses = course.syllabuses
        enrollment_count = Enrollment.query.filter_by(course_id=course_id).count()
        
        return render_template('public/course_detail.html',
                             course=course,
                             videos=videos,
                             syllabuses=syllabuses,
                             enrollment_count=enrollment_count)
    except Exception as e:
        print(f"Error loading course detail: {e}")
        flash('Error loading course. Please try again.', 'danger')
        return redirect(url_for('public.courses'))

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Page"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()
            
            # Validation
            if not all([name, email, subject, message]):
                flash('Please fill in all fields!', 'danger')
                return redirect(url_for('public.contact'))
            
            if len(name) < 2 or len(name) > 100:
                flash('Name must be between 2 and 100 characters!', 'danger')
                return redirect(url_for('public.contact'))
            
            if not is_valid_email(email):
                flash('Please enter a valid email address!', 'danger')
                return redirect(url_for('public.contact'))
            
            if len(subject) < 3 or len(subject) > 200:
                flash('Subject must be between 3 and 200 characters!', 'danger')
                return redirect(url_for('public.contact'))
            
            if len(message) < 5 or len(message) > 1000:
                flash('Message must be between 5 and 1000 characters!', 'danger')
                return redirect(url_for('public.contact'))
            
            try:
                contact_msg = ContactMessage(name=name, email=email, subject=subject, message=message)
                db.session.add(contact_msg)
                db.session.commit()
                flash('Your message has been sent successfully! We will get back to you soon.', 'success')
                return redirect(url_for('public.contact'))
            except Exception as db_error:
                db.session.rollback()
                print(f"Database error: {db_error}")
                flash('Error sending message. Please try again.', 'danger')
                return redirect(url_for('public.contact'))
        except Exception as e:
            print(f"Error processing contact form: {e}")
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('public.contact'))
    
    # Get recent messages for display
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template('public/contact.html', recent_messages=recent_messages)

@public_bp.route('/about')
def about():
    """About Us Page"""
    return render_template('public/about.html')

@public_bp.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    """Deprecated chatbot endpoint kept for backward compatibility."""
    try:
        data = request.get_json(silent=True) or {}
        
        if not data or 'message' not in data:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        user_message = data.get('message', '').strip()
        course_id = data.get('course_id')
        domain = data.get('domain')
        current_page = data.get('current_page')
        course_name = data.get('course_name')
        
        if not user_message:
            return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400
        
        if len(user_message) > 500:
            return jsonify({'success': False, 'error': 'Message is too long (max 500 characters)'}), 400
        
        payload = build_rulebased_chatbot_payload(
            user_message,
            context={
                'page': current_page,
                'course': course_name,
                'domain': domain,
                'course_id': course_id,
            },
            user_id=session.get('user_id'),
        )
        bot_response = payload.get('answer') or payload.get('response') or ''
        options = payload.get('options') or []
        
        # Store conversation in database (optional - for analytics)
        try:
            user_id = session.get('user_id') if 'user_id' in session else None
            conversation = ChatbotConversation(
                user_id=user_id,
                course_id=course_id,
                user_message=user_message,
                bot_response=bot_response,
                domain=domain
            )
            db.session.add(conversation)
            db.session.commit()
        except Exception as db_error:
            print(f"Error storing conversation: {db_error}")
            # Continue even if storage fails - don't block the assistant
        
        return jsonify({
            'success': True,
            'data': {
                'answer': bot_response,
                'agent': payload.get('agent', 'rulebased_mentor'),
                'options': options,
                'suggestions': options,
            },
            'message': user_message,
            'response': bot_response,
            'answer': bot_response,
            'options': options,
            'agent': payload.get('agent', 'rulebased_mentor'),
            'suggestions': options,
            'deprecated': True,
            'deprecated_in_favor_of': '/api/chat',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        print(f"AI Learning Assistant Error: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your question'
        }), 500

# Error Handlers
@public_bp.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@public_bp.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@public_bp.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400


