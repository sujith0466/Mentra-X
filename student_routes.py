from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import (
    db, User, Course, Enrollment, ReferralTransaction, Video, Syllabus, Domain,
    LessonProgress, LearningStreak, Quiz, Assignment, CommunityPost, CourseModule, UserBadge, UserXP, UserResume
)
from datetime import datetime
from functools import wraps
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_, func
import io
import os
import re
from learning_utils import mark_lesson_complete
from services.ai.recommendation_service import recommend_courses
from services.ai.ml.learning_difficulty_model import detect_learning_difficulty
from services.ai.ml.skill_prediction_model import predict_next_skills
from services.ai.assistant_service import get_available_agents
from services.ai.learning_feed_service import generate_learning_feed
from services.ai.learning.learning_insights_service import get_learning_insights
from services.ai.skills.skill_graph_service import get_dashboard_skill_progress
from services.ai.career.resume_service import CAREER_SKILL_MAP
from services.ai.project_idea_service import generate_project_ideas
from services.profile_service import load_profile, save_profile
from services.wallet_service import get_wallet_balance
from services.reward_service import build_reward_history, get_referral_rewards
import json

student_bp = Blueprint('student', __name__, url_prefix='/student')


def _is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email or "") is not None


def _parse_list_input(value: str) -> list:
    cleaned = (value or "").replace("\n", ",")
    items = [item.strip() for item in cleaned.split(",") if item.strip()]
    return items

def _visible_courses_query():
    """Student browse list: published courses only, excluding temp/test titles."""
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


def _visible_domains_query():
    return Domain.query.filter(~Domain.name.ilike('qa domain%'))

# Authentication decorator for student routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'student':
            flash('Access denied! Student account required.', 'danger')
            return redirect(url_for('public.index'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@student_required
def dashboard():
    """Student Dashboard"""
    try:
        user = db.session.get(User, session['user_id'])
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.login'))
        
        enrollments = (
            Enrollment.query
            .options(joinedload(Enrollment.course))
            .filter_by(user_id=user.id)
            .order_by(Enrollment.enrolled_date.desc())
            .all()
        )
        referral_count = ReferralTransaction.query.filter_by(referrer_id=user.id).count()
        streak = LearningStreak.query.filter_by(user_id=user.id).first()

        def course_image_src(course):
            image_value = (course.image_url or '').strip() if course else ''
            if not image_value:
                return None
            if image_value.startswith(('http://', 'https://', '/static/')):
                return image_value
            if image_value.startswith('static/'):
                return url_for('static', filename=image_value.replace('static/', '', 1))
            return url_for('static', filename=f'images/courses/{os.path.basename(image_value)}')

        enrolled_ids = [enrollment.course_id for enrollment in enrollments if enrollment.course_id]
        lesson_count_map = {}
        if enrolled_ids:
            lesson_count_rows = (
                db.session.query(Video.course_id, func.count(Video.id))
                .filter(Video.course_id.in_(enrolled_ids))
                .group_by(Video.course_id)
                .all()
            )
            lesson_count_map = {course_id: int(count) for course_id, count in lesson_count_rows}

        enrolled_courses = []
        enrollment_completion_changed = False
        for enrollment in enrollments:
            course = enrollment.course
            if not course:
                continue
            progress = int(round(enrollment.progress_percentage if enrollment.progress_percentage is not None else (enrollment.progress or 0)))
            total_lessons = lesson_count_map.get(course.id, 0)
            completed_lessons = int(round((progress / 100.0) * total_lessons)) if total_lessons else 0
            desired_completed = progress >= 100
            if bool(enrollment.completed) != desired_completed:
                enrollment.completed = desired_completed
                enrollment_completion_changed = True
            is_completed = bool(enrollment.completed or progress >= 100)
            enrolled_courses.append({
                'enrollment': enrollment,
                'course': course,
                'progress': max(0, min(progress, 100)),
                'completed': is_completed,
                'completed_lessons': completed_lessons,
                'total_lessons': total_lessons,
                'image_src': course_image_src(course),
                'short_description': ((course.description or '').strip()[:120] + '...') if course.description and len(course.description.strip()) > 120 else (course.description or 'No description available.'),
            })
        if enrollment_completion_changed:
            db.session.commit()

        total_enrolled = len(enrolled_courses)
        completed_courses = sum(1 for row in enrolled_courses if row['completed'])
        in_progress_courses = sum(1 for row in enrolled_courses if row['progress'] > 0 and not row['completed'])

        next_lesson_by_course = {}
        if enrolled_ids:
            next_lesson_rows = (
                Video.query
                .outerjoin(
                    LessonProgress,
                    and_(
                        LessonProgress.lesson_id == Video.id,
                        LessonProgress.user_id == user.id,
                    ),
                )
                .filter(Video.course_id.in_(enrolled_ids))
                .filter(or_(LessonProgress.completed.is_(False), LessonProgress.completed.is_(None)))
                .order_by(Video.course_id.asc(), Video.order_number.asc(), Video.id.asc())
                .all()
            )
            for video in next_lesson_rows:
                if video.course_id not in next_lesson_by_course:
                    next_lesson_by_course[video.course_id] = video

        continue_learning = None
        for row in enrolled_courses:
            if row['completed']:
                continue
            row['next_lesson'] = next_lesson_by_course.get(row['course'].id)
            continue_learning = row
            break
        if continue_learning is None and enrolled_courses:
            continue_learning = enrolled_courses[0]

        recommended_payload = []
        service_recommendations = recommend_courses(user.id)
        recommended_courses = []
        recommended_ids = [item.get('id') for item in service_recommendations if item.get('id')]
        recommended_map = {}
        if recommended_ids:
            recommended_rows = Course.query.filter(Course.id.in_(recommended_ids)).all()
            recommended_map = {course.id: course for course in recommended_rows}

        for item in service_recommendations:
            course = recommended_map.get(item.get('id'))
            if course:
                recommended_courses.append((course, item.get('reason', 'Recommended for your next step.')))

        if not recommended_courses:
            fallback_query = Course.query
            if enrolled_ids:
                fallback_query = fallback_query.filter(~Course.id.in_(enrolled_ids))
            fallback_courses = (
                fallback_query
                .filter(or_(Course.status == 'published', Course.status == None))
                .order_by(Course.created_at.desc())
                .limit(6)
                .all()
            )
            recommended_courses = [(course, 'Popular next-step course from the catalog.') for course in fallback_courses]

        for course, reason in recommended_courses[:6]:
            rating = 4.1 + ((course.id % 9) * 0.1)
            recommended_payload.append({
                'course': course,
                'image_src': course_image_src(course),
                'rating': round(min(rating, 4.9), 1),
                'reason': reason,
            })

        certificates = [row for row in enrolled_courses if row['completed']]
        badges = []
        if total_enrolled >= 1:
            badges.append('Starter Learner')
        if in_progress_courses >= 2:
            badges.append('Consistency Streak')
        if completed_courses >= 1:
            badges.append('Course Finisher')
        if completed_courses >= 5:
            badges.append('Master Achiever')
        if referral_count >= 1:
            badges.append('Community Builder')

        recent_activity = []
        for row in enrolled_courses:
            course = row['course']
            enrollment = row['enrollment']
            if enrollment.enrolled_date:
                recent_activity.append({
                    'time': enrollment.enrolled_date,
                    'text': f'Enrolled in {course.title}',
                    'type': 'enrollment',
                })
            if row['progress'] > 0 and not row['completed']:
                recent_activity.append({
                    'time': enrollment.enrolled_date or datetime.utcnow(),
                    'text': f'Completed {row["progress"]}% of {course.title}',
                    'type': 'lesson',
                })
            if row['completed']:
                completed_time = enrollment.enrolled_date or datetime.utcnow()
                recent_activity.append({
                    'time': completed_time,
                    'text': f'Earned certificate in {course.title}',
                    'type': 'certificate',
                })

        if referral_count > 0:
            recent_activity.append({
                'time': datetime.utcnow(),
                'text': f'Earned referral rewards from {referral_count} successful invites',
                'type': 'reward',
            })

        recent_activity = sorted(recent_activity, key=lambda item: item['time'], reverse=True)[:8]
        progress_chart_rows = [
            {'label': row['course'].title, 'value': row['progress']}
            for row in enrolled_courses[:8]
        ]
        try:
            difficulty_payload = detect_learning_difficulty(user.id) or {}
        except Exception:
            difficulty_payload = {}

        try:
            skill_prediction = predict_next_skills(user.id) or {}
        except Exception:
            skill_prediction = {}

        try:
            skill_progress = get_dashboard_skill_progress(user.id, limit=8) or []
        except Exception:
            skill_progress = []

        try:
            ai_learning_feed = generate_learning_feed(
                user.id,
                difficulty_payload=difficulty_payload,
                skill_snapshot=skill_progress,
                skill_prediction=skill_prediction,
            )
        except Exception:
            ai_learning_feed = []

        xp_profile = UserXP.query.filter_by(user_id=user.id).first()
        earned_badges = UserBadge.query.filter_by(user_id=user.id).order_by(UserBadge.awarded_at.desc(), UserBadge.id.desc()).limit(6).all()
        community_posts = CommunityPost.query.order_by(CommunityPost.created_at.desc(), CommunityPost.id.desc()).limit(5).all()
        ai_agents = get_available_agents()
        level_thresholds = [0, 100, 300, 600]
        current_level = xp_profile.level if xp_profile else 1
        current_xp = xp_profile.xp_points if xp_profile else 0
        current_threshold = level_thresholds[min(max(current_level - 1, 0), len(level_thresholds) - 1)]
        next_threshold = level_thresholds[min(current_level, len(level_thresholds) - 1)] if current_level < len(level_thresholds) else current_threshold + 300
        span = max(1, next_threshold - current_threshold)
        level_progress_percentage = round(((current_xp - current_threshold) / span) * 100, 2) if next_threshold > current_threshold else 100.0

        try:
            ai_learning_insights = get_learning_insights(user.id)
        except Exception:
            ai_learning_insights = {
                'weak_topics': difficulty_payload.get('weak_topics', [])[:3],
                'recommended_courses': [item['course'].title for item in recommended_payload[:3]],
                'suggested_skills': skill_prediction.get('skills_to_learn_next', [])[:3],
            }

        resume_row = UserResume.query.filter_by(user_id=user.id).first()
        resume_insights = None
        if resume_row:
            detected_skills = json.loads(resume_row.skills_json or "[]")
            career_scores = []
            for career, required_skills in CAREER_SKILL_MAP.items():
                score = sum(1 for skill in required_skills if skill in detected_skills)
                if score > 0:
                    career_scores.append((career, score))
            career_scores.sort(key=lambda item: item[1], reverse=True)
            primary_career = career_scores[0][0] if career_scores else "Full Stack Developer"
            recommended_skills = [
                skill for skill in CAREER_SKILL_MAP.get(primary_career, [])
                if skill not in detected_skills
            ]
            domain = "AI"
            if any(skill in detected_skills for skill in ["React", "JavaScript", "HTML", "CSS"]):
                domain = "Web Development"
            elif any(skill in detected_skills for skill in ["Machine Learning", "Deep Learning", "Neural Networks"]):
                domain = "AI"
            elif any(skill in detected_skills for skill in ["Pandas", "Statistics", "Visualization"]):
                domain = "Data Science"
            project_ideas = generate_project_ideas(domain, user_id=user.id)
            resume_insights = {
                "detected_skills": detected_skills[:6],
                "recommended_skills": recommended_skills[:6],
                "project_suggestions": [item["title"] for item in project_ideas[:3]],
            }

        return render_template(
            'student/dashboard.html',
            user=user,
            today_date=datetime.utcnow(),
            enrolled_courses=enrolled_courses,
            total_enrolled=total_enrolled,
            in_progress_courses=in_progress_courses,
            completed_courses=completed_courses,
            wallet_balance=float(user.wallet_balance or 0.0),
            continue_learning=continue_learning,
            recommended_courses=recommended_payload,
            certificates=certificates,
            badges=badges,
            recent_activity=recent_activity,
            referral_count=referral_count,
            learning_streak=streak.current_streak if streak else 0,
            longest_streak=streak.longest_streak if streak else 0,
            progress_chart_rows=progress_chart_rows,
            learning_feed=ai_learning_feed,
            ai_learning_feed=ai_learning_feed,
            skill_progress=skill_progress,
            ai_learning_insights=ai_learning_insights,
            resume_insights=resume_insights,
            xp_profile=xp_profile,
            earned_badges=earned_badges,
            community_posts=community_posts,
            ai_agents=ai_agents,
            level_progress_percentage=level_progress_percentage,
        )
    except Exception as e:
        print(f"Error loading student dashboard: {e}")
        flash('Error loading dashboard. Please try again.', 'danger')
        return redirect(url_for('public.index'))


@student_bp.route('/certificate/<int:course_id>/download')
@student_required
def download_certificate(course_id):
    """Download PDF certificate for completed courses."""
    try:
        user = User.query.get(session['user_id'])
        enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first_or_404()
        current_progress = enrollment.progress_percentage if enrollment.progress_percentage is not None else (enrollment.progress or 0)
        if not (enrollment.completed or current_progress >= 100):
            flash('Certificate is available only for completed courses.', 'warning')
            return redirect(url_for('student.dashboard'))

        course = Course.query.get_or_404(course_id)
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas

        issued_on = datetime.utcnow().strftime('%Y-%m-%d')
        certificate_id = f"CERT-{course.id}-{user.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        pdf.setTitle('Course Completion Certificate')
        pdf.setLineWidth(2)
        pdf.rect(0.6 * inch, 0.6 * inch, width - 1.2 * inch, height - 1.2 * inch)

        logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            pdf.drawImage(logo_path, width / 2 - 0.8 * inch, height - 1.6 * inch, width=1.6 * inch, height=1.0 * inch, preserveAspectRatio=True, mask='auto')

        pdf.setFont('Helvetica-Bold', 24)
        pdf.drawCentredString(width / 2, height - 2.3 * inch, 'Certificate of Completion')
        pdf.setFont('Helvetica', 14)
        pdf.drawCentredString(width / 2, height - 3.1 * inch, 'This certifies that')
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawCentredString(width / 2, height - 3.8 * inch, user.name)
        pdf.setFont('Helvetica', 14)
        pdf.drawCentredString(width / 2, height - 4.5 * inch, 'has successfully completed')
        pdf.setFont('Helvetica-Bold', 18)
        pdf.drawCentredString(width / 2, height - 5.2 * inch, course.title)
        pdf.setFont('Helvetica', 12)
        pdf.drawCentredString(width / 2, height - 6.0 * inch, f'Completion Date: {issued_on}')
        pdf.drawCentredString(width / 2, height - 6.4 * inch, f'Instructor: {course.instructor or "Education Portal Faculty"}')
        pdf.drawCentredString(width / 2, height - 6.8 * inch, f'Certificate ID: {certificate_id}')
        pdf.save()
        buffer.seek(0)
        filename = f"certificate_{course.id}_{user.id}.pdf"
        return (
            buffer.getvalue(),
            200,
            {
                'Content-Type': 'application/pdf',
                'Content-Disposition': f'attachment; filename={filename}',
            },
        )
    except Exception as e:
        print(f"Error downloading certificate: {e}")
        flash('Unable to download certificate right now.', 'danger')
        return redirect(url_for('student.dashboard'))

@student_bp.route('/my-courses')
@student_required
def my_courses():
    """View Enrolled Courses"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.login'))
        
        # Get all enrollments with course details
        enrollments = Enrollment.query.filter_by(user_id=user.id).all()
        courses = [enrollment.course for enrollment in enrollments]
        
        return render_template('student/my_courses.html', courses=courses, enrollments=enrollments)
    except Exception as e:
        print(f"Error loading my courses: {e}")
        flash('Error loading courses. Please try again.', 'danger')
        return redirect(url_for('student.dashboard'))

@student_bp.route('/courses')
def browse_courses():
    """Browse All Courses (Public - Anyone Can Browse)"""
    try:
        # Get all domains for filter
        domains = _visible_domains_query().all()
        
        # Get filter from query parameters
        domain_filter = request.args.get('domain', type=int)
        search_query = request.args.get('search', '').strip()
        
        query = _visible_courses_query()
        if domain_filter:
            query = query.filter(Course.domain_id == domain_filter)
        if search_query:
            query = query.filter(
                (Course.title.ilike(f'%{search_query}%')) |
                (Course.description.ilike(f'%{search_query}%'))
            )
        courses = query.order_by(Course.created_at.desc()).all()
        
        return render_template('student/courses.html', 
                             courses=courses, 
                             domains=domains,
                             domain_filter=domain_filter,
                             search_query=search_query)
    except Exception as e:
        print(f"Error loading courses: {e}")
        flash('Error loading courses. Please try again.', 'danger')
        return redirect(url_for('public.index'))

@student_bp.route('/course/<int:course_id>/details')
def course_details(course_id):
    """View Course Details (Public - Anyone Can View Before Enrolling)"""
    try:
        course = Course.query.get_or_404(course_id)
        
        # Get course syllabus
        syllabus = Syllabus.query.filter_by(course_id=course_id).order_by(Syllabus.order_number).all()
        modules = CourseModule.query.filter_by(course_id=course_id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()
        module_map = {module.id: {'module': module, 'lessons': [], 'quizzes': [], 'assignments': []} for module in modules}
        for video in Video.query.filter_by(course_id=course_id).order_by(Video.order_number.asc(), Video.id.asc()).all():
            if video.module_id in module_map:
                module_map[video.module_id]['lessons'].append(video)
        for quiz in Quiz.query.filter_by(course_id=course_id, is_enabled=True).order_by(Quiz.created_at.asc()).all():
            if quiz.module_id in module_map:
                module_map[quiz.module_id]['quizzes'].append(quiz)
        for assignment in Assignment.query.filter_by(course_id=course_id).order_by(Assignment.created_at.asc()).all():
            if assignment.module_id in module_map:
                module_map[assignment.module_id]['assignments'].append(assignment)
        course_modules = [module_map[module.id] for module in modules]
        
        # Check if user is logged in and already enrolled
        is_enrolled = False
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first()
                is_enrolled = enrollment is not None
        
        return render_template('student/course_details.html', 
                             course=course, 
                             syllabus=syllabus,
                             course_modules=course_modules,
                             is_enrolled=is_enrolled)
    except Exception as e:
        print(f"Error loading course details: {e}")
        flash('Error loading course details. Please try again.', 'danger')
        return redirect(url_for('student.browse_courses'))

@student_bp.route('/course/<int:course_id>')
@student_required
def course_videos(course_id):
    """View Course Videos (Only for Enrolled Students)"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.login'))
        
        course = Course.query.get_or_404(course_id)
        
        # Check if student is enrolled
        enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first()
        if not enrollment:
            flash('You must enroll in this course to view videos!', 'danger')
            return redirect(url_for('student.my_courses'))
        
        # Get videos and syllabus
        videos = Video.query.filter_by(course_id=course_id).order_by(Video.order_number).all()
        videos_payload = [
            {
                'id': video.id,
                'title': video.title,
                'video_url': video.video_url,
                'description': video.description or '',
                'duration': video.duration or '',
            }
            for video in videos
        ]
        syllabuses = course.syllabuses
        quiz_count = Quiz.query.filter_by(course_id=course_id, is_enabled=True).count()
        assignment_count = Assignment.query.filter_by(course_id=course_id).count()
        completed_lesson_ids = {
            row.lesson_id for row in LessonProgress.query.filter_by(user_id=user.id, course_id=course_id, completed=True).all()
        }
        modules = CourseModule.query.filter_by(course_id=course_id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()
        module_map = {module.id: {'module': module, 'lessons': [], 'quizzes': [], 'assignments': []} for module in modules}
        for video in videos:
            if video.module_id in module_map:
                module_map[video.module_id]['lessons'].append(video)
        for quiz in Quiz.query.filter_by(course_id=course_id, is_enabled=True).order_by(Quiz.created_at.asc()).all():
            if quiz.module_id in module_map:
                module_map[quiz.module_id]['quizzes'].append(quiz)
        for assignment in Assignment.query.filter_by(course_id=course_id).order_by(Assignment.created_at.asc()).all():
            if assignment.module_id in module_map:
                module_map[assignment.module_id]['assignments'].append(assignment)
        course_modules = [module_map[module.id] for module in modules]
        
        return render_template('student/course_videos.html', 
                             course=course, 
                             videos=videos, 
                             syllabuses=syllabuses,
                             enrollment=enrollment,
                             quiz_count=quiz_count,
                             assignment_count=assignment_count,
                             completed_lesson_ids=completed_lesson_ids,
                             videos_payload=videos_payload,
                             course_modules=course_modules)
    except Exception as e:
        print(f"Error loading course videos: {e}")
        flash('Error loading course. Please try again.', 'danger')
        return redirect(url_for('student.my_courses'))

@student_bp.route('/enroll/<int:course_id>', methods=['POST'])
@student_required
def enroll_course(course_id):
    """Enroll in a Course"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.login'))
        
        course = Course.query.get_or_404(course_id)
        
        # Check if already enrolled
        existing_enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first()
        if existing_enrollment:
            flash('You are already enrolled in this course!', 'warning')
            return redirect(url_for('student.course_videos', course_id=course_id))
        
        # Create enrollment
        enrollment = Enrollment(user_id=user.id, course_id=course_id, progress=0.0, progress_percentage=0.0)
        db.session.add(enrollment)
        db.session.commit()
        
        flash(f'Successfully enrolled in {course.title}!', 'success')
        return redirect(url_for('student.course_videos', course_id=course_id))
    except Exception as e:
        db.session.rollback()
        print(f"Error enrolling in course: {e}")
        flash('Error enrolling in course. Please try again.', 'danger')
        return redirect(url_for('public.courses'))



@student_bp.route('/profile/edit', methods=['GET', 'POST'])
@student_required
def edit_profile():
    # Edit student profile details without schema changes.
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.login'))

        profile_payload = load_profile(user.id)
        bio = profile_payload.get('bio', '')
        skills = profile_payload.get('skills', [])
        learning_goals = profile_payload.get('learning_goals', [])

        if request.method == 'POST':
            name = (request.form.get('name') or '').strip()
            email = (request.form.get('email') or '').strip()
            bio = (request.form.get('bio') or '').strip()
            skills_input = request.form.get('skills') or ''
            goals_input = request.form.get('learning_goals') or ''

            if not name:
                flash('Name cannot be empty.', 'danger')
                return redirect(url_for('student.edit_profile'))

            if not _is_valid_email(email):
                flash('Please enter a valid email address.', 'danger')
                return redirect(url_for('student.edit_profile'))

            existing = User.query.filter(User.email == email, User.id != user.id).first()
            if existing:
                flash('This email is already used by another account.', 'danger')
                return redirect(url_for('student.edit_profile'))

            user.name = name
            user.email = email
            db.session.commit()

            skills = _parse_list_input(skills_input)
            learning_goals = _parse_list_input(goals_input)
            save_profile(user.id, bio=bio, skills=skills, learning_goals=learning_goals)

            session['user_name'] = user.name
            session['user_email'] = user.email

            flash('Profile updated successfully.', 'success')
            return redirect(url_for('student.edit_profile'))

        return render_template(
            'student/profile/edit_profile.html',
            user=user,
            bio=bio,
            skills_text=", ".join(skills),
            learning_goals_text="\n".join(learning_goals),
        )
    except Exception as e:
        db.session.rollback()
        print(f"Error updating profile: {e}")
        flash('Error updating profile. Please try again.', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/referral')
@student_required
def referral():
    """Referral Program Page"""
    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('auth.login'))

        referrals = get_referral_rewards(user.id)
        referral_count = len(referrals)
        total_earnings = sum(ref.reward_amount for ref in referrals)

        referred_users = build_reward_history(referrals)
        wallet_balance = get_wallet_balance(user.id)

        referral_link = url_for('referral.accept_referral', referral_code=user.referral_code, _external=True)

        return render_template(
            'student/referral.html',
            user=user,
            referral_code=user.referral_code,
            referral_link=referral_link,
            referral_count=referral_count,
            total_earnings=total_earnings,
            referred_users=referred_users,
            wallet_balance=wallet_balance,
        )
    except Exception as e:
        print(f"Error loading referral page: {e}")
        flash('Error loading referral page. Please try again.', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/update-progress/<int:course_id>', methods=['POST'])
@student_required
def update_progress(course_id):
    """Update Course Progress"""
    try:
        user = User.query.get(session['user_id'])
        progress = request.form.get('progress', 0)
        
        enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first_or_404()
        progress_value = float(progress)
        enrollment.progress = progress_value
        enrollment.progress_percentage = progress_value
        
        if progress_value >= 100:
            enrollment.completed = True
        
        db.session.commit()
        flash('Progress updated successfully!', 'success')
        return redirect(url_for('student.course_videos', course_id=course_id))
    except Exception as e:
        db.session.rollback()
        print(f"Error updating progress: {e}")
        flash('Error updating progress. Please try again.', 'danger')
        return redirect(url_for('student.my_courses'))


@student_bp.route('/course/<int:course_id>/lesson/<int:lesson_id>/complete', methods=['POST'])
@student_required
def complete_lesson(course_id, lesson_id):
    """Mark lesson as completed and update streak/progress."""
    try:
        user = User.query.get(session['user_id'])
        enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course_id).first()
        if not enrollment:
            flash('You must enroll in this course first.', 'danger')
            return redirect(url_for('student.course_details', course_id=course_id))

        lesson = Video.query.filter_by(id=lesson_id, course_id=course_id).first_or_404()
        mark_lesson_complete(user.id, course_id, lesson.id)
        db.session.commit()
        flash(f'Lesson "{lesson.title}" marked as complete.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error completing lesson: {e}")
        flash('Could not mark lesson complete.', 'danger')
    return redirect(url_for('student.course_videos', course_id=course_id))






