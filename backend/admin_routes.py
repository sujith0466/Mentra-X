from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, Response
from backend.models import db, User, Domain, Course, Syllabus, Video, Enrollment, ReferralTransaction, AdminUser, AuditLog, CourseModule, Quiz, Assignment, UserResume
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import joinedload, selectinload
from backend.audit_utils import log_audit
import csv
import io
import math
import os
import secrets
import uuid
import json
import re

from backend.services.ai.career.resume_service import CAREER_SKILL_MAP

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
COURSE_STATUSES = ('draft', 'review', 'published', 'archived')
ADMIN_ROLES = ('super_admin', 'content_admin', 'support_analyst')
ADMIN_SESSION_TIMEOUT_SECONDS = 1800
ENFORCE_ADMIN_PASSWORD_ROTATION = False
ADMIN_PASSWORD_MAX_AGE_DAYS = 90
REQUIRE_DESTRUCTIVE_APPROVAL = True
DEFAULT_PAGE_SIZE = 15

ADMIN_ROLE_PERMISSIONS = {
    'super_admin': {'*'},
    'content_admin': {
        'dashboard',
        'manage_courses',
        'add_course',
        'edit_course',
        'delete_course',
        'course_view',
        'inline_update_course',
        'manage_syllabus',
        'add_syllabus',
        'update_syllabus',
        'delete_syllabus',
        'reorder_syllabus',
        'manage_videos',
        'add_video',
        'update_video',
        'delete_video',
        'reorder_videos',
        'add_course_module',
        'edit_course_module',
        'delete_course_module',
        'reorder_course_modules',
        'update_content_module',
        'manage_domains',
        'add_domain',
        'delete_domain',
        'bulk_course_action',
        'export_courses_csv',
        'admin_activity',
        'audit_logs',
        'system_alerts',
        'export_enrollments_csv',
        'export_referrals_csv',
        'quizzes_overview',
        'manage_course_quizzes',
        'add_quiz',
        'edit_quiz',
        'delete_quiz',
        'manage_quiz_questions',
        'add_quiz_question',
        'edit_quiz_question',
        'delete_quiz_question',
        'reorder_quiz_questions',
        'import_quiz_questions_from_paste',
        'import_quiz_questions_from_file',
        'generate_quiz_from_lesson',
        'assignments_overview',
        'manage_course_assignments',
        'add_assignment',
        'edit_assignment',
        'delete_assignment',
        'assignment_submissions',
        'grade_submission',
    },
    'support_analyst': {
        'dashboard',
        'manage_students',
        'view_enrollments',
        'view_referrals',
        'export_enrollments_csv',
        'export_referrals_csv',
        'admin_activity',
        'system_alerts',
        'audit_logs',
    },
}



def _images_directory():
    images_dir = os.path.join(admin_bp.root_path, 'static', 'images', 'courses')
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def _is_allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def _save_course_image(file_storage, course_title):
    if not file_storage or not file_storage.filename:
        return None

    original_name = secure_filename(file_storage.filename)
    if not original_name or not _is_allowed_image(original_name):
        return None

    extension = original_name.rsplit('.', 1)[1].lower()
    base_title = secure_filename((course_title or 'course').lower().replace(' ', '-')) or 'course'
    filename = f"{base_title}-{uuid.uuid4().hex[:8]}.{extension}"
    save_path = os.path.join(_images_directory(), filename)
    file_storage.save(save_path)
    return filename


def _delete_course_image_if_local(image_value):
    if not image_value:
        return
    if image_value.startswith(('http://', 'https://', '/static/', 'static/')):
        return

    file_name = os.path.basename(image_value)
    image_path = os.path.join(_images_directory(), file_name)
    if os.path.isfile(image_path):
        os.remove(image_path)


def _resolve_admin_course_image(course):
    image_value = (course.image_url or '').strip()
    if not image_value:
        return None
    if image_value.startswith(('http://', 'https://')):
        return image_value
    file_name = os.path.basename(image_value)
    image_path = os.path.join(_images_directory(), file_name)
    if os.path.isfile(image_path):
        return url_for('static', filename=f'images/courses/{file_name}')
    return None


def _parse_int(value, default=1, min_value=1):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(parsed, min_value)


def _parse_float(value):
    if value is None or str(value).strip() == '':
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _paginate_query(query, page, per_page):
    total = query.order_by(None).count()
    pages = max(1, math.ceil(total / per_page)) if total else 1
    page = min(page, pages)
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
        'items': items,
        'total': total,
        'pages': pages,
        'page': page,
        'per_page': per_page,
        'has_prev': page > 1,
        'has_next': page < pages,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page < pages else None,
    }


def _normalize_course_status(value):
    status = (value or 'draft').strip().lower()
    return status if status in COURSE_STATUSES else 'draft'


def _normalized_name(value):
    return ' '.join((value or '').strip().split()).lower()


def _looks_like_test_or_random_name(value):
    text = (value or '').strip()
    lowered = text.lower()
    if not text:
        return True
    if lowered.startswith(('qa domain', 'qa course', 'test ', 'temp ')):
        return True
    if re.search(r'\b[0-9a-f]{8,}\b', lowered):
        return True
    return False


def _validate_domain_name(name):
    cleaned = (name or '').strip()
    if len(cleaned) < 3 or len(cleaned) > 100:
        return False, 'Domain name must be between 3 and 100 characters.'
    if not re.match(r'^[A-Za-z][A-Za-z0-9 &()\-+/]{2,99}$', cleaned):
        return False, 'Domain name can contain letters, numbers, spaces, and &() - + /.'
    if _looks_like_test_or_random_name(cleaned):
        return False, 'Domain name looks like temporary/test data. Please use a real domain name.'
    return True, ''


def _validate_course_title(title):
    cleaned = (title or '').strip()
    if len(cleaned) < 3 or len(cleaned) > 100:
        return False, 'Course title must be between 3 and 100 characters.'
    if not re.match(r'^[A-Za-z][A-Za-z0-9 &()\-+:/.]{2,99}$', cleaned):
        return False, 'Course title contains invalid characters.'
    if _looks_like_test_or_random_name(cleaned):
        return False, 'Course title looks like temporary/test data. Please use a real course title.'
    return True, ''


def _domain_exists_by_normalized_name(name, exclude_domain_id=None):
    normalized = _normalized_name(name)
    if not normalized:
        return False
    query = Domain.query.with_entities(Domain.id, Domain.name)
    if exclude_domain_id is not None:
        query = query.filter(Domain.id != exclude_domain_id)
    for row in query.all():
        if _normalized_name(row.name) == normalized:
            return True
    return False


def _course_exists_in_domain(title, domain_id, exclude_course_id=None):
    normalized = _normalized_name(title)
    if not normalized:
        return False
    query = Course.query.with_entities(Course.id, Course.title).filter(Course.domain_id == domain_id)
    if exclude_course_id is not None:
        query = query.filter(Course.id != exclude_course_id)
    for row in query.all():
        if _normalized_name(row.title) == normalized:
            return True
    return False


def _course_noise_match_expression():
    return or_(
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


def _validate_course_payload(title, description, instructor, price_value, demo_video_url):
    errors = []
    title_ok, title_error = _validate_course_title(title)
    if not title_ok:
        errors.append(title_error)
    if description and len(description) > 1000:
        errors.append('Course description cannot exceed 1000 characters.')
    if instructor and (len(instructor) < 2 or len(instructor) > 100):
        errors.append('Instructor name must be between 2 and 100 characters when provided.')
    if price_value is None or price_value < 0:
        errors.append('Price must be a valid non-negative number.')
    if demo_video_url and not (
        demo_video_url.startswith('https://')
        and ('youtube.com' in demo_video_url or 'youtu.be' in demo_video_url or 'vimeo.com' in demo_video_url)
    ):
        errors.append('Demo video URL must be a valid YouTube or Vimeo URL using HTTPS.')
    return errors


def _can_publish_course(course):
    syllabus_count = Syllabus.query.filter_by(course_id=course.id).count()
    video_count = Video.query.filter_by(course_id=course.id).count()
    return syllabus_count > 0 and video_count > 0


def _next_module_order(course_id):
    current_max = db.session.query(func.max(CourseModule.order_index)).filter(CourseModule.course_id == course_id).scalar()
    return int(current_max or 0) + 1


def _course_snapshot(course):
    return {
        'id': course.id,
        'title': course.title,
        'domain_id': course.domain_id,
        'price': course.price,
        'instructor': course.instructor,
        'status': course.status,
        'demo_video_url': course.demo_video_url,
    }


def _get_content_quality_alerts():
    stale_cutoff = datetime.utcnow() - timedelta(days=30)

    syllabus_counts = (
        db.session.query(Syllabus.course_id, func.count(Syllabus.id).label('count'))
        .group_by(Syllabus.course_id)
        .subquery()
    )
    video_counts = (
        db.session.query(Video.course_id, func.count(Video.id).label('count'))
        .group_by(Video.course_id)
        .subquery()
    )

    missing_syllabus = (
        db.session.query(func.count(Course.id))
        .outerjoin(syllabus_counts, syllabus_counts.c.course_id == Course.id)
        .filter(func.coalesce(syllabus_counts.c.count, 0) == 0)
        .scalar()
        or 0
    )
    missing_videos = (
        db.session.query(func.count(Course.id))
        .outerjoin(video_counts, video_counts.c.course_id == Course.id)
        .filter(func.coalesce(video_counts.c.count, 0) == 0)
        .scalar()
        or 0
    )
    stale_courses = (
        db.session.query(func.count(Course.id))
        .filter(Course.status.in_(('draft', 'review')), Course.created_at <= stale_cutoff)
        .scalar()
        or 0
    )

    alerts = []
    if missing_syllabus:
        alerts.append({'level': 'warning', 'message': f'{missing_syllabus} courses are missing syllabus topics.'})
    if missing_videos:
        alerts.append({'level': 'warning', 'message': f'{missing_videos} courses are missing videos.'})
    if stale_courses:
        alerts.append({'level': 'info', 'message': f'{stale_courses} draft/review courses are older than 30 days.'})

    return {
        'missing_syllabus': int(missing_syllabus),
        'missing_videos': int(missing_videos),
        'stale_courses': int(stale_courses),
        'alerts': alerts,
    }


def _require_destructive_confirmation():
    if not REQUIRE_DESTRUCTIVE_APPROVAL:
        return True
    return (request.form.get('confirm_phrase') or '').strip().upper() == 'DELETE'


def _get_admin_profile():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return AdminUser.query.filter_by(user_id=user_id).first()


def _validate_admin_password_strength(password):
    if not password or len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    if not any(ch.isupper() for ch in password):
        return False, 'Password must include at least one uppercase letter.'
    if not any(ch.islower() for ch in password):
        return False, 'Password must include at least one lowercase letter.'
    if not any(ch.isdigit() for ch in password):
        return False, 'Password must include at least one digit.'
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(ch in special_chars for ch in password):
        return False, 'Password must include at least one special character.'
    return True, ''


def _ensure_csrf_token():
    token = session.get('csrf_token')
    if not token:
        token = secrets.token_urlsafe(32)
        session['csrf_token'] = token
    return token


@admin_bp.before_request
def admin_security_checks():
    endpoint = (request.endpoint or '').replace('admin.', '')
    if endpoint == 'static':
        return None
    if 'user_id' not in session:
        return None

    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        return None

    profile = _get_admin_profile()
    if not profile:
        flash('Admin profile not found.', 'danger')
        session.clear()
        return redirect(url_for('auth.login'))

    admin_role = (profile.role or session.get('admin_role') or 'super_admin').strip().lower()
    if admin_role not in ADMIN_ROLES:
        admin_role = 'super_admin'
    session['admin_role'] = admin_role

    # Session timeout for admin users.
    now = datetime.utcnow()
    last_seen_raw = session.get('admin_last_seen')
    if last_seen_raw:
        try:
            last_seen = datetime.fromisoformat(last_seen_raw)
            if (now - last_seen).total_seconds() > ADMIN_SESSION_TIMEOUT_SECONDS:
                session.clear()
                flash('Admin session expired. Please login again.', 'warning')
                return redirect(url_for('auth.login'))
        except ValueError:
            pass
    session['admin_last_seen'] = now.isoformat()

    # Optional password rotation policy.
    if ENFORCE_ADMIN_PASSWORD_ROTATION and profile.password_changed_at:
        password_age = (now - profile.password_changed_at).days
        if password_age > ADMIN_PASSWORD_MAX_AGE_DAYS and endpoint not in {'edit_admin', 'manage_admins'}:
            flash('Password rotation required. Update your admin password.', 'warning')
            return redirect(url_for('admin.edit_admin', admin_id=profile.id))

    # RBAC permission check.
    allowed = ADMIN_ROLE_PERMISSIONS.get(admin_role, set())
    if '*' not in allowed and endpoint not in allowed:
        log_audit(entity_type='security', action_type='rbac_denied', metadata={'endpoint': endpoint})
        flash('Access denied for your admin role.', 'danger')
        return redirect(url_for('admin.dashboard'))

    # CSRF protection for admin POST requests.
    if request.method == 'POST':
        session_token = _ensure_csrf_token()
        request_token = (
            request.form.get('csrf_token')
            or request.headers.get('X-CSRF-Token')
            or request.headers.get('X-CSRFToken')
        )
        if not request_token or request_token != session_token:
            log_audit(entity_type='security', action_type='csrf_failure', metadata={'endpoint': endpoint})
            flash('Invalid CSRF token. Please refresh and try again.', 'danger')
            return redirect(request.referrer or url_for('admin.dashboard'))

    return None


@admin_bp.context_processor
def inject_admin_security_context():
    role = session.get('admin_role', 'super_admin')
    allowed = ADMIN_ROLE_PERMISSIONS.get(role, set())
    can_access = lambda endpoint: ('*' in allowed) or (endpoint in allowed)
    quick_links = [
        {'label': 'Courses', 'endpoint': 'admin.manage_courses'},
        {'label': 'Draft Courses', 'endpoint': 'admin.manage_courses', 'params': {'status': 'draft'}},
        {'label': 'Students', 'endpoint': 'admin.manage_students'},
        {'label': 'Enrollments', 'endpoint': 'admin.view_enrollments'},
    ]
    if role == 'super_admin':
        quick_links.append({'label': 'Admin Users', 'endpoint': 'admin.manage_admins'})
    return {
        'csrf_token': _ensure_csrf_token(),
        'admin_session_timeout_seconds': ADMIN_SESSION_TIMEOUT_SECONDS,
        'admin_role': role,
        'admin_sidebar_links': quick_links,
        'admin_can_access': can_access,
    }

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Access denied! Admin account required.', 'danger')
            return redirect(url_for('public.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin Dashboard"""
    try:
        # Get statistics
        total_users = User.query.filter_by(role='student').count()
        total_courses = Course.query.count()
        total_domains = Domain.query.filter(~Domain.name.ilike('qa domain%')).count()
        total_enrollments = Enrollment.query.count()

        # Get recent enrollments
        recent_enrollments = (
            Enrollment.query
            .options(joinedload(Enrollment.student), joinedload(Enrollment.course))
            .order_by(Enrollment.enrolled_date.desc())
            .limit(10)
            .all()
        )
        lifecycle_counts = {
            row[0]: row[1]
            for row in (
                db.session.query(Course.status, func.count(Course.id))
                .group_by(Course.status)
                .all()
            )
        }
        quality_alerts = _get_content_quality_alerts()

        resume_rows = UserResume.query.all()
        resume_upload_count = len(resume_rows)
        resume_upload_rate = round((resume_upload_count / total_users) * 100, 2) if total_users else 0.0
        skill_counts = {}
        missing_counts = {}
        for row in resume_rows:
            skills = json.loads(row.skills_json or "[]")
            for skill in skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
            career_scores = []
            for career, required in CAREER_SKILL_MAP.items():
                score = sum(1 for skill in required if skill in skills)
                if score > 0:
                    career_scores.append((career, score))
            career_scores.sort(key=lambda item: item[1], reverse=True)
            primary_career = career_scores[0][0] if career_scores else "Full Stack Developer"
            missing = [skill for skill in CAREER_SKILL_MAP[primary_career] if skill not in skills]
            for skill in missing:
                missing_counts[skill] = missing_counts.get(skill, 0) + 1

        top_skills = [
            {
                "skill": skill,
                "percent": round((count / resume_upload_count) * 100, 1) if resume_upload_count else 0.0,
            }
            for skill, count in sorted(skill_counts.items(), key=lambda item: item[1], reverse=True)[:5]
        ]
        top_missing = [skill for skill, _ in sorted(missing_counts.items(), key=lambda item: item[1], reverse=True)[:5]]

        return render_template('admin/dashboard.html',
                             total_users=total_users,
                             total_courses=total_courses,
                             total_domains=total_domains,
                             total_enrollments=total_enrollments,
                             lifecycle_counts=lifecycle_counts,
                             quality_alerts=quality_alerts,
                             recent_enrollments=recent_enrollments,
                             resume_upload_count=resume_upload_count,
                             resume_upload_rate=resume_upload_rate,
                             top_resume_skills=top_skills,
                             top_missing_skills=top_missing)
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        flash('Error loading dashboard. Please try again.', 'danger')
        return redirect(url_for('public.index'))


@admin_bp.route('/course/<int:course_id>/view')
@admin_required
def course_view(course_id):
    """Admin Course Preview"""
    course = (
        Course.query
        .options(
            joinedload(Course.domain),
            selectinload(Course.syllabuses),
            selectinload(Course.videos),
        )
        .get_or_404(course_id)
    )
    # Defensive: fetch syllabus and videos in order
    syllabuses = course.syllabuses if hasattr(course, 'syllabuses') else []
    videos = course.videos if hasattr(course, 'videos') else []
    return render_template(
        'admin/course_view.html',
        course=course,
        syllabuses=syllabuses,
        videos=videos
    )


@admin_bp.route('/course/<int:course_id>/modules/add', methods=['POST'])
@admin_required
def add_course_module(course_id):
    course = Course.query.get_or_404(course_id)
    title = request.form.get('title', '').strip()
    if not title:
        flash('Module title is required.', 'danger')
        return redirect(url_for('admin.edit_course', course_id=course.id))
    try:
        order_index = request.form.get('order_index', type=int) or _next_module_order(course.id)
        module = CourseModule(course_id=course.id, title=title, order_index=max(1, order_index))
        db.session.add(module)
        db.session.commit()
        flash('Module added.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error adding module: {e}")
        flash('Could not add module.', 'danger')
    return redirect(url_for('admin.edit_course', course_id=course.id))


@admin_bp.route('/module/<int:module_id>/edit', methods=['POST'])
@admin_required
def edit_course_module(module_id):
    module = CourseModule.query.get_or_404(module_id)
    try:
        title = request.form.get('title', '').strip()
        if title:
            module.title = title
        order_index = request.form.get('order_index', type=int)
        if order_index is not None and order_index > 0:
            module.order_index = order_index
        db.session.commit()
        flash('Module updated.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error editing module: {e}")
        flash('Could not update module.', 'danger')
    return redirect(url_for('admin.edit_course', course_id=module.course_id))


@admin_bp.route('/module/<int:module_id>/delete', methods=['POST'])
@admin_required
def delete_course_module(module_id):
    module = CourseModule.query.get_or_404(module_id)
    course_id = module.course_id
    try:
        Video.query.filter_by(module_id=module.id).update({'module_id': None})
        Quiz.query.filter_by(module_id=module.id).update({'module_id': None})
        Assignment.query.filter_by(module_id=module.id).update({'module_id': None})
        db.session.delete(module)
        db.session.commit()
        flash('Module deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting module: {e}")
        flash('Could not delete module.', 'danger')
    return redirect(url_for('admin.edit_course', course_id=course_id))


@admin_bp.route('/course/<int:course_id>/modules/reorder', methods=['POST'])
@admin_required
def reorder_course_modules(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json(silent=True) or {}
    ordered_ids = data.get('ordered_ids') or []
    modules = CourseModule.query.filter_by(course_id=course.id).all()
    valid_ids = {m.id for m in modules}
    if set(ordered_ids) != valid_ids:
        return jsonify({'success': False, 'error': 'Invalid module ids'}), 400
    try:
        module_map = {m.id: m for m in modules}
        for idx, module_id in enumerate(ordered_ids, start=1):
            module_map[module_id].order_index = idx
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Error reordering modules: {e}")
        return jsonify({'success': False, 'error': 'Could not reorder modules'}), 500


@admin_bp.route('/course/<int:course_id>/content-module/update', methods=['POST'])
@admin_required
def update_content_module(course_id):
    course = Course.query.get_or_404(course_id)
    content_type = (request.form.get('content_type') or '').strip().lower()
    content_id = request.form.get('content_id', type=int)
    module_id = request.form.get('module_id', type=int)
    if module_id is not None:
        module = CourseModule.query.filter_by(id=module_id, course_id=course.id).first()
        if not module:
            flash('Invalid module selected.', 'danger')
            return redirect(url_for('admin.edit_course', course_id=course.id))

    model_map = {
        'lesson': Video,
        'quiz': Quiz,
        'assignment': Assignment,
    }
    model = model_map.get(content_type)
    if not model or not content_id:
        flash('Invalid content update request.', 'danger')
        return redirect(url_for('admin.edit_course', course_id=course.id))

    item = model.query.filter_by(id=content_id, course_id=course.id).first()
    if not item:
        flash('Content item not found.', 'danger')
        return redirect(url_for('admin.edit_course', course_id=course.id))
    try:
        item.module_id = module_id
        db.session.commit()
        flash('Module assignment updated.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error updating content module: {e}")
        flash('Could not update module assignment.', 'danger')
    return redirect(url_for('admin.edit_course', course_id=course.id))

@admin_bp.route('/domains')
@admin_required
def manage_domains():
    """Manage Domains"""
    try:
        domains = (
            Domain.query
            .options(selectinload(Domain.courses))
            .filter(~Domain.name.ilike('qa domain%'))
            .order_by(Domain.name.asc())
            .all()
        )
        metric_rows = (
            db.session.query(
                Domain.id.label('domain_id'),
                func.count(func.distinct(Course.id)).label('course_count'),
                func.count(func.distinct(Enrollment.user_id)).label('student_count'),
            )
            .outerjoin(Course, Course.domain_id == Domain.id)
            .outerjoin(Enrollment, Enrollment.course_id == Course.id)
            .group_by(Domain.id)
            .all()
        )
        domain_metrics = {
            row.domain_id: {
                'course_count': row.course_count or 0,
                'student_count': row.student_count or 0,
            }
            for row in metric_rows
        }
        return render_template('admin/manage_domains.html', domains=domains, domain_metrics=domain_metrics)
    except Exception as e:
        print(f"Error loading domains: {e}")
        flash('Error loading domains. Please try again.', 'danger')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/domain/add', methods=['POST'])
@admin_required
def add_domain():
    """Add New Domain"""
    try:
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Domain name is required!', 'danger')
            return redirect(url_for('admin.manage_domains'))

        is_valid_name, validation_error = _validate_domain_name(name)
        if not is_valid_name:
            flash(validation_error, 'danger')
            return redirect(url_for('admin.manage_domains'))

        if _domain_exists_by_normalized_name(name):
            flash('Domain already exists (same name with different casing/spaces).', 'danger')
            return redirect(url_for('admin.manage_domains'))
        
        domain = Domain(name=name, description=description)
        db.session.add(domain)
        db.session.commit()
        
        flash(f'Domain "{name}" added successfully!', 'success')
        return redirect(url_for('admin.manage_domains'))
    except Exception as e:
        db.session.rollback()
        print(f"Error adding domain: {e}")
        flash('Error adding domain. Please try again.', 'danger')
        return redirect(url_for('admin.manage_domains'))


@admin_bp.route('/domain/<int:domain_id>/delete', methods=['POST'])
@admin_required
def delete_domain(domain_id):
    if not _require_destructive_confirmation():
        flash('Delete confirmation phrase required.', 'danger')
        return redirect(url_for('admin.manage_domains'))
    try:
        domain = Domain.query.get_or_404(domain_id)
        before_values = {'id': domain.id, 'name': domain.name}
        db.session.delete(domain)
        db.session.commit()
        log_audit(entity_type='domain', entity_id=domain_id, action_type='delete', before=before_values, after=None)
        flash(f'Domain "{before_values["name"]}" deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting domain: {e}")
        flash('Error deleting domain. Please try again.', 'danger')
    return redirect(url_for('admin.manage_domains'))

@admin_bp.route('/courses')
@admin_required
def manage_courses():
    """Manage Courses"""
    try:
        page = _parse_int(request.args.get('page'), default=1)
        per_page = DEFAULT_PAGE_SIZE
        search = request.args.get('search', '').strip()
        domain_id = request.args.get('domain', '').strip()
        min_price = _parse_float(request.args.get('min_price'))
        max_price = _parse_float(request.args.get('max_price'))
        has_demo = request.args.get('has_demo', '').strip().lower()
        content_filter = request.args.get('content', '').strip().lower()
        status_filter = request.args.get('status', '').strip().lower()
        sort_key = request.args.get('sort', 'created_at').strip().lower()
        sort_dir = request.args.get('dir', 'desc').strip().lower()

        syllabus_counts = (
            db.session.query(
                Syllabus.course_id.label('course_id'),
                func.count(Syllabus.id).label('syllabus_count'),
            )
            .group_by(Syllabus.course_id)
            .subquery()
        )
        video_counts = (
            db.session.query(
                Video.course_id.label('course_id'),
                func.count(Video.id).label('video_count'),
            )
            .group_by(Video.course_id)
            .subquery()
        )
        enrollment_counts = (
            db.session.query(
                Enrollment.course_id.label('course_id'),
                func.count(Enrollment.id).label('enrollment_count'),
            )
            .group_by(Enrollment.course_id)
            .subquery()
        )

        syllabus_count_col = func.coalesce(syllabus_counts.c.syllabus_count, 0)
        video_count_col = func.coalesce(video_counts.c.video_count, 0)
        enrollment_count_col = func.coalesce(enrollment_counts.c.enrollment_count, 0)

        query = (
            db.session.query(
                Course,
                syllabus_count_col.label('syllabus_count'),
                video_count_col.label('video_count'),
                enrollment_count_col.label('enrollment_count'),
            )
            .join(Domain, Course.domain_id == Domain.id)
            .outerjoin(syllabus_counts, syllabus_counts.c.course_id == Course.id)
            .outerjoin(video_counts, video_counts.c.course_id == Course.id)
            .outerjoin(enrollment_counts, enrollment_counts.c.course_id == Course.id)
            .options(joinedload(Course.domain))
        )
        query = query.filter(~_course_noise_match_expression())

        if search:
            query = query.filter(
                or_(
                    Course.title.ilike(f'%{search}%'),
                    Course.instructor.ilike(f'%{search}%'),
                )
            )

        if domain_id:
            domain_id_int = _parse_int(domain_id, default=0, min_value=0)
            if domain_id_int:
                query = query.filter(Course.domain_id == domain_id_int)

        if min_price is not None:
            query = query.filter(Course.price >= min_price)
        if max_price is not None:
            query = query.filter(Course.price <= max_price)

        if has_demo in {'yes', 'no'}:
            if has_demo == 'yes':
                query = query.filter(Course.demo_video_url.isnot(None), Course.demo_video_url != '')
            else:
                query = query.filter(or_(Course.demo_video_url.is_(None), Course.demo_video_url == ''))

        if content_filter:
            if content_filter == 'syllabus':
                query = query.filter(syllabus_count_col > 0)
            elif content_filter == 'videos':
                query = query.filter(video_count_col > 0)
            elif content_filter == 'both':
                query = query.filter(and_(syllabus_count_col > 0, video_count_col > 0))
            elif content_filter == 'any':
                query = query.filter(or_(syllabus_count_col > 0, video_count_col > 0))
            elif content_filter == 'none':
                query = query.filter(and_(syllabus_count_col == 0, video_count_col == 0))

        has_status = hasattr(Course, 'status')
        if has_status and status_filter:
            query = query.filter(func.lower(Course.status) == status_filter)

        sort_columns = {
            'title': Course.title,
            'instructor': Course.instructor,
            'domain': Domain.name,
            'price': Course.price,
            'syllabus_count': syllabus_count_col,
            'video_count': video_count_col,
            'enrollment_count': enrollment_count_col,
            'created_at': Course.created_at,
        }
        if has_status:
            sort_columns['status'] = Course.status

        if sort_key not in sort_columns:
            sort_key = 'created_at'
        if sort_dir not in {'asc', 'desc'}:
            sort_dir = 'desc'

        order_expr = sort_columns[sort_key].asc() if sort_dir == 'asc' else sort_columns[sort_key].desc()
        query = query.order_by(order_expr, Course.id.desc())

        pagination = _paginate_query(query, page=page, per_page=per_page)
        domains = Domain.query.filter(~Domain.name.ilike('qa domain%')).order_by(Domain.name.asc()).all()
        status_options = []
        if has_status:
            status_options = [
                row[0]
                for row in db.session.query(Course.status)
                .filter(Course.status.isnot(None), Course.status != '')
                .distinct()
                .order_by(Course.status.asc())
                .all()
            ]
        lifecycle_counts = {}
        if has_status:
            lifecycle_counts = {
                row[0]: row[1]
                for row in (
                    db.session.query(Course.status, func.count(Course.id))
                    .group_by(Course.status)
                    .all()
                )
            }

        return render_template(
            'admin/manage_courses.html',
            course_rows=pagination['items'],
            pagination=pagination,
            domains=domains,
            has_status=has_status,
            status_options=status_options,
            lifecycle_counts=lifecycle_counts,
            filters={
                'search': search,
                'domain': domain_id,
                'min_price': request.args.get('min_price', '').strip(),
                'max_price': request.args.get('max_price', '').strip(),
                'has_demo': has_demo,
                'content': content_filter,
                'status': status_filter,
                'sort': sort_key,
                'dir': sort_dir,
            },
        )
    except Exception as e:
        print(f"Error loading courses: {e}")
        flash('Error loading courses. Please try again.', 'danger')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/courses/bulk-action', methods=['POST'])
@admin_required
def bulk_course_action():
    """Bulk publish/review/archive courses."""
    try:
        action = (request.form.get('bulk_action') or '').strip().lower()
        selected_ids_raw = request.form.get('selected_course_ids', '').strip()
        if not selected_ids_raw:
            flash('No courses selected for bulk action.', 'warning')
            return redirect(url_for('admin.manage_courses'))

        valid_actions = {
            'publish': 'published',
            'review': 'review',
            'archive': 'archived',
        }
        if action not in valid_actions:
            flash('Invalid bulk action selected.', 'danger')
            return redirect(url_for('admin.manage_courses'))

        course_ids = []
        for item in selected_ids_raw.split(','):
            try:
                parsed = int(item.strip())
                if parsed > 0:
                    course_ids.append(parsed)
            except ValueError:
                continue
        if not course_ids:
            flash('No valid courses selected.', 'warning')
            return redirect(url_for('admin.manage_courses'))

        courses = Course.query.filter(Course.id.in_(course_ids)).all()
        updated = 0
        skipped_publish_guard = 0
        for course in courses:
            before = _course_snapshot(course)
            target_status = valid_actions[action]
            if target_status == 'published' and not _can_publish_course(course):
                skipped_publish_guard += 1
                continue
            course.status = target_status
            updated += 1
            db.session.flush()
            log_audit(
                entity_type='course',
                entity_id=course.id,
                action_type=f'bulk_{action}',
                before=before,
                after=_course_snapshot(course),
            )

        db.session.commit()
        if updated:
            flash(f'Bulk action completed for {updated} course(s).', 'success')
        if skipped_publish_guard:
            flash(
                f'{skipped_publish_guard} course(s) skipped publish guard (missing syllabus/videos).',
                'warning',
            )
    except Exception as e:
        db.session.rollback()
        print(f"Error in bulk course action: {e}")
        flash('Error processing bulk action.', 'danger')

    return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/exports/courses.csv')
@admin_required
def export_courses_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'title', 'domain', 'instructor', 'price', 'status', 'created_at'])
    rows = (
        db.session.query(Course, Domain.name)
        .join(Domain, Course.domain_id == Domain.id)
        .order_by(Course.created_at.desc())
        .all()
    )
    for course, domain_name in rows:
        writer.writerow([
            course.id,
            course.title,
            domain_name,
            course.instructor or '',
            course.price or 0,
            course.status or 'draft',
            course.created_at.isoformat() if course.created_at else '',
        ])
    output.seek(0)
    log_audit(entity_type='report', action_type='export_courses_csv', metadata={'count': len(rows)})
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=courses_export.csv'},
    )


@admin_bp.route('/exports/enrollments.csv')
@admin_required
def export_enrollments_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'student_name', 'student_email', 'course', 'enrolled_date', 'progress', 'completed'])
    rows = (
        Enrollment.query
        .options(joinedload(Enrollment.student), joinedload(Enrollment.course))
        .order_by(Enrollment.enrolled_date.desc())
        .all()
    )
    for row in rows:
        writer.writerow([
            row.id,
            row.student.name if row.student else '',
            row.student.email if row.student else '',
            row.course.title if row.course else '',
            row.enrolled_date.isoformat() if row.enrolled_date else '',
            row.progress,
            row.completed,
        ])
    output.seek(0)
    log_audit(entity_type='report', action_type='export_enrollments_csv', metadata={'count': len(rows)})
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=enrollments_export.csv'},
    )


@admin_bp.route('/exports/referrals.csv')
@admin_required
def export_referrals_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'referrer', 'new_user', 'reward_amount', 'status', 'date'])
    rows = (
        ReferralTransaction.query
        .options(joinedload(ReferralTransaction.referrer), joinedload(ReferralTransaction.new_user))
        .order_by(ReferralTransaction.date.desc())
        .all()
    )
    for row in rows:
        writer.writerow([
            row.id,
            row.referrer.name if row.referrer else '',
            row.new_user.name if row.new_user else '',
            row.reward_amount,
            row.status,
            row.date.isoformat() if row.date else '',
        ])
    output.seek(0)
    log_audit(entity_type='report', action_type='export_referrals_csv', metadata={'count': len(rows)})
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=referrals_export.csv'},
    )


@admin_bp.route('/activity')
@admin_required
def admin_activity():
    page = _parse_int(request.args.get('page'), default=1)
    logs_query = AuditLog.query.options(joinedload(AuditLog.actor)).order_by(AuditLog.created_at.desc())
    pagination = _paginate_query(logs_query, page=page, per_page=20)
    return render_template('admin/admin_activity.html', logs=pagination['items'], pagination=pagination)


@admin_bp.route('/audit-logs')
@admin_required
def audit_logs():
    page = _parse_int(request.args.get('page'), default=1)
    logs_query = AuditLog.query.options(joinedload(AuditLog.actor)).order_by(AuditLog.created_at.desc())
    pagination = _paginate_query(logs_query, page=page, per_page=30)
    return render_template('admin/audit_logs.html', logs=pagination['items'], pagination=pagination)


@admin_bp.route('/system-alerts')
@admin_required
def system_alerts():
    quality = _get_content_quality_alerts()
    recent_errors = (
        AuditLog.query
        .filter(AuditLog.action_type.in_(['error', 'csrf_failure', 'rate_limit']))
        .order_by(AuditLog.created_at.desc())
        .limit(20)
        .all()
    )
    return render_template('admin/system_alerts.html', quality=quality, recent_errors=recent_errors)

@admin_bp.route('/course/add', methods=['POST'])
@admin_required
def add_course():
    """Add New Course"""
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        domain_id = request.form.get('domain_id', '')
        price = request.form.get('price', 0)
        instructor = request.form.get('instructor', '').strip()
        image_url = request.form.get('image_url', '').strip()
        demo_video_url = request.form.get('demo_video_url', '').strip()
        status = _normalize_course_status(request.form.get('status', 'draft'))
        image_file = request.files.get('course_image')
        
        if not all([title, domain_id]):
            flash('Title and Domain are required!', 'danger')
            return redirect(url_for('admin.manage_courses'))
        
        domain = Domain.query.get_or_404(domain_id)
        if _course_exists_in_domain(title, domain.id):
            flash('Course already exists in this domain (same name with different casing/spaces).', 'danger')
            return redirect(url_for('admin.manage_courses'))

        price_value = _parse_float(price)
        validation_errors = _validate_course_payload(title, description, instructor, price_value, demo_video_url)
        if status == 'published':
            validation_errors.append('New course cannot be published before adding syllabus and videos.')
        if validation_errors:
            for err in validation_errors:
                flash(err, 'danger')
            return redirect(url_for('admin.manage_courses'))

        uploaded_image_name = None
        if image_file and image_file.filename:
            uploaded_image_name = _save_course_image(image_file, title)
            if not uploaded_image_name:
                flash('Invalid image format. Allowed: png, jpg, jpeg, webp, gif.', 'danger')
                return redirect(url_for('admin.manage_courses'))
        
        course = Course(
            title=title,
            description=description,
            domain_id=domain_id,
            price=price_value or 0,
            instructor=instructor,
            image_url=uploaded_image_name or image_url,
            demo_video_url=demo_video_url,
            status=status,
        )
        db.session.add(course)
        db.session.commit()
        log_audit(
            entity_type='course',
            entity_id=course.id,
            action_type='create',
            after=_course_snapshot(course),
        )
        
        flash(f'Course "{title}" added successfully!', 'success')
        return redirect(url_for('admin.manage_courses'))
    except Exception as e:
        db.session.rollback()
        print(f"Error adding course: {e}")
        flash('Error adding course. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))

@admin_bp.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_bp.route('/course/<int:course_id>/builder', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    """Edit Course"""
    course = Course.query.get_or_404(course_id)
    domains = Domain.query.all()
    
    if request.method == 'POST':
        try:
            before_snapshot = _course_snapshot(course)
            old_image_value = course.image_url
            course.title = request.form.get('title', '').strip()
            course.description = request.form.get('description', '').strip()
            requested_domain_raw = request.form.get('domain_id', course.domain_id)
            requested_price = _parse_float(request.form.get('price', 0))
            course.instructor = request.form.get('instructor', '').strip()
            image_url_input = request.form.get('image_url', '').strip()
            image_file = request.files.get('course_image')
            requested_status = _normalize_course_status(request.form.get('status', course.status or 'draft'))
            demo_video_url = request.form.get('demo_video_url', '').strip()
            requested_domain_id = None
            if str(requested_domain_raw).isdigit():
                requested_domain_id = int(requested_domain_raw)

            validation_errors = _validate_course_payload(
                course.title,
                course.description,
                course.instructor,
                requested_price,
                demo_video_url,
            )
            if requested_domain_id is None:
                validation_errors.append('Please select a valid domain.')
            elif not Domain.query.get(requested_domain_id):
                validation_errors.append('Selected domain does not exist.')

            if requested_domain_id is not None and _course_exists_in_domain(
                course.title,
                requested_domain_id,
                exclude_course_id=course.id,
            ):
                validation_errors.append('Another course with the same title already exists in this domain.')
            if requested_status == 'published' and not _can_publish_course(course):
                validation_errors.append('Cannot publish course without at least one syllabus topic and one video.')
            if validation_errors:
                for err in validation_errors:
                    flash(err, 'danger')
                return redirect(url_for('admin.edit_course', course_id=course_id))

            course.domain_id = requested_domain_id
            course.price = requested_price or 0
            course.status = requested_status

            if image_file and image_file.filename:
                uploaded_image_name = _save_course_image(image_file, course.title)
                if not uploaded_image_name:
                    flash('Invalid image format. Allowed: png, jpg, jpeg, webp, gif.', 'danger')
                    return redirect(url_for('admin.edit_course', course_id=course_id))
                course.image_url = uploaded_image_name
                _delete_course_image_if_local(old_image_value)
            elif image_url_input:
                course.image_url = image_url_input

            course.demo_video_url = demo_video_url
            
            db.session.commit()
            action_type = 'update'
            if before_snapshot.get('status') != course.status and course.status in {'published', 'archived'}:
                action_type = f'status_{course.status}'
            log_audit(
                entity_type='course',
                entity_id=course.id,
                action_type=action_type,
                before=before_snapshot,
                after=_course_snapshot(course),
            )
            flash('Course updated successfully!', 'success')
            return redirect(url_for('admin.manage_courses'))
        except Exception as e:
            db.session.rollback()
            print(f"Error editing course: {e}")
            flash('Error updating course. Please try again.', 'danger')
    
    current_image_url = _resolve_admin_course_image(course)
    modules = CourseModule.query.filter_by(course_id=course.id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()
    lessons = Video.query.filter_by(course_id=course.id).order_by(Video.order_number.asc(), Video.id.asc()).all()
    quizzes = Quiz.query.filter_by(course_id=course.id).order_by(Quiz.created_at.asc()).all()
    assignments = Assignment.query.filter_by(course_id=course.id).order_by(Assignment.created_at.asc()).all()
    return render_template(
        'admin/edit_course.html',
        course=course,
        domains=domains,
        current_image_url=current_image_url,
        course_statuses=COURSE_STATUSES,
        modules=modules,
        lessons=lessons,
        quizzes=quizzes,
        assignments=assignments,
    )

@admin_bp.route('/course/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    """Delete Course"""
    if not _require_destructive_confirmation():
        flash('Delete confirmation phrase required.', 'danger')
        return redirect(url_for('admin.manage_courses'))
    try:
        course = Course.query.get_or_404(course_id)
        before_snapshot = _course_snapshot(course)
        title = course.title
        _delete_course_image_if_local(course.image_url)
        db.session.delete(course)
        db.session.commit()
        log_audit(
            entity_type='course',
            entity_id=course_id,
            action_type='delete',
            before=before_snapshot,
            after=None,
        )
        flash(f'Course "{title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting course: {e}")
        flash('Error deleting course. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/course/<int:course_id>/inline-update', methods=['POST'])
@admin_required
def inline_update_course(course_id):
    """Fast inline update for course list."""
    try:
        course = Course.query.get_or_404(course_id)
        before_snapshot = _course_snapshot(course)
        instructor = request.form.get('instructor', '').strip()
        price_value = _parse_float(request.form.get('price', 0))
        status = _normalize_course_status(request.form.get('status', course.status or 'draft'))

        validation_errors = _validate_course_payload(
            course.title,
            course.description or '',
            instructor,
            price_value,
            course.demo_video_url or '',
        )
        if status == 'published' and not _can_publish_course(course):
            validation_errors.append('Cannot publish course without at least one syllabus topic and one video.')
        if validation_errors:
            for err in validation_errors:
                flash(err, 'danger')
            return redirect(url_for('admin.manage_courses', **request.args.to_dict()))

        course.instructor = instructor
        course.price = price_value or 0
        course.status = status
        db.session.commit()
        action_type = 'inline_update'
        if before_snapshot.get('status') != course.status and course.status in {'published', 'archived'}:
            action_type = f'status_{course.status}'
        log_audit(
            entity_type='course',
            entity_id=course.id,
            action_type=action_type,
            before=before_snapshot,
            after=_course_snapshot(course),
        )
        flash('Course updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error in inline course update: {e}")
        flash('Error updating course inline. Please try again.', 'danger')

    return redirect(url_for('admin.manage_courses', **request.args.to_dict()))

@admin_bp.route('/course/<int:course_id>/syllabus')
@admin_required
def manage_syllabus(course_id):
    """Manage Course Syllabus"""
    try:
        course = Course.query.get_or_404(course_id)
        syllabuses = Syllabus.query.filter_by(course_id=course_id).order_by(Syllabus.order_number).all()
        return render_template('admin/manage_syllabus.html', course=course, syllabuses=syllabuses)
    except Exception as e:
        print(f"Error loading syllabus: {e}")
        flash('Error loading syllabus. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/course/<int:course_id>/syllabus/reorder', methods=['POST'])
@admin_required
def reorder_syllabus(course_id):
    """Reorder syllabus topics using drag and drop."""
    course = Course.query.get_or_404(course_id)
    data = request.get_json(silent=True) or {}
    ordered_ids = data.get('ordered_ids') or []
    if not isinstance(ordered_ids, list):
        return jsonify({'success': False, 'error': 'Invalid payload'}), 400

    valid_topics = Syllabus.query.filter_by(course_id=course.id).all()
    valid_ids = {topic.id for topic in valid_topics}
    if set(ordered_ids) != valid_ids:
        return jsonify({'success': False, 'error': 'Invalid syllabus ids'}), 400

    try:
        for idx, topic_id in enumerate(ordered_ids, start=1):
            topic = next((t for t in valid_topics if t.id == topic_id), None)
            if topic:
                topic.order_number = idx
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Error reordering syllabus: {e}")
        return jsonify({'success': False, 'error': 'Could not reorder syllabus'}), 500

@admin_bp.route('/syllabus/add', methods=['POST'])
@admin_required
def add_syllabus():
    """Add Syllabus Topic"""
    try:
        course_id = request.form.get('course_id', '')
        topic_title = request.form.get('topic_title', '').strip()
        topic_description = request.form.get('topic_description', '').strip()
        order_number = request.form.get('order_number', 0)
        
        if not all([course_id, topic_title]):
            flash('Course and Topic Title are required!', 'danger')
            return redirect(url_for('admin.manage_syllabus', course_id=course_id))
        if len(topic_title) < 3 or len(topic_title) > 200:
            flash('Topic title must be between 3 and 200 characters.', 'danger')
            return redirect(url_for('admin.manage_syllabus', course_id=course_id))
        if topic_description and len(topic_description) > 1000:
            flash('Topic description cannot exceed 1000 characters.', 'danger')
            return redirect(url_for('admin.manage_syllabus', course_id=course_id))
        order_number_int = _parse_int(order_number, default=0, min_value=0)
        
        syllabus = Syllabus(
            course_id=course_id,
            topic_title=topic_title,
            topic_description=topic_description,
            order_number=order_number_int
        )
        db.session.add(syllabus)
        db.session.commit()
        
        flash('Syllabus topic added successfully!', 'success')
        return redirect(url_for('admin.manage_syllabus', course_id=course_id))
    except Exception as e:
        db.session.rollback()
        print(f"Error adding syllabus: {e}")
        flash('Error adding syllabus topic. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/syllabus/<int:syllabus_id>/update', methods=['POST'])
@admin_required
def update_syllabus(syllabus_id):
    """Update Syllabus Topic"""
    try:
        syllabus = Syllabus.query.get_or_404(syllabus_id)
        course_id = syllabus.course_id

        topic_title = request.form.get('topic_title', '').strip()
        topic_description = request.form.get('topic_description', '').strip()
        order_number = request.form.get('order_number', syllabus.order_number)

        if not topic_title:
            flash('Topic title is required!', 'danger')
            return redirect(url_for('admin.manage_syllabus', course_id=course_id))
        if len(topic_title) < 3 or len(topic_title) > 200:
            flash('Topic title must be between 3 and 200 characters.', 'danger')
            return redirect(url_for('admin.manage_syllabus', course_id=course_id))
        if topic_description and len(topic_description) > 1000:
            flash('Topic description cannot exceed 1000 characters.', 'danger')
            return redirect(url_for('admin.manage_syllabus', course_id=course_id))

        syllabus.topic_title = topic_title
        syllabus.topic_description = topic_description
        syllabus.order_number = _parse_int(order_number, default=0, min_value=0)

        db.session.commit()
        flash('Syllabus topic updated successfully!', 'success')
        return redirect(url_for('admin.manage_syllabus', course_id=course_id))
    except Exception as e:
        db.session.rollback()
        print(f"Error updating syllabus: {e}")
        flash('Error updating syllabus topic. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/syllabus/<int:syllabus_id>/delete', methods=['POST'])
@admin_required
def delete_syllabus(syllabus_id):
    """Delete Syllabus Topic"""
    if not _require_destructive_confirmation():
        flash('Delete confirmation phrase required.', 'danger')
        syllabus = Syllabus.query.get_or_404(syllabus_id)
        return redirect(url_for('admin.manage_syllabus', course_id=syllabus.course_id))
    try:
        syllabus = Syllabus.query.get_or_404(syllabus_id)
        course_id = syllabus.course_id
        db.session.delete(syllabus)
        db.session.commit()
        flash('Syllabus topic deleted successfully!', 'success')
        return redirect(url_for('admin.manage_syllabus', course_id=course_id))
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting syllabus: {e}")
        flash('Error deleting syllabus topic. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))

@admin_bp.route('/course/<int:course_id>/videos')
@admin_required
def manage_videos(course_id):
    """Manage Course Videos"""
    try:
        course = Course.query.get_or_404(course_id)
        videos = Video.query.filter_by(course_id=course_id).order_by(Video.order_number).all()
        modules = CourseModule.query.filter_by(course_id=course_id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()
        return render_template('admin/manage_videos.html', course=course, videos=videos, modules=modules)
    except Exception as e:
        print(f"Error loading videos: {e}")
        flash('Error loading videos. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/course/<int:course_id>/videos/reorder', methods=['POST'])
@admin_required
def reorder_videos(course_id):
    """Reorder videos using drag and drop."""
    course = Course.query.get_or_404(course_id)
    data = request.get_json(silent=True) or {}
    ordered_ids = data.get('ordered_ids') or []
    if not isinstance(ordered_ids, list):
        return jsonify({'success': False, 'error': 'Invalid payload'}), 400

    valid_videos = Video.query.filter_by(course_id=course.id).all()
    valid_ids = {video.id for video in valid_videos}
    if set(ordered_ids) != valid_ids:
        return jsonify({'success': False, 'error': 'Invalid video ids'}), 400

    try:
        for idx, video_id in enumerate(ordered_ids, start=1):
            video = next((v for v in valid_videos if v.id == video_id), None)
            if video:
                video.order_number = idx
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Error reordering videos: {e}")
        return jsonify({'success': False, 'error': 'Could not reorder videos'}), 500

@admin_bp.route('/video/add', methods=['POST'])
@admin_required
def add_video():
    """Add Video to Course"""
    try:
        course_id = request.form.get('course_id', '')
        title = request.form.get('title', '').strip()
        video_url = request.form.get('video_url', '').strip()
        description = request.form.get('description', '').strip()
        duration = request.form.get('duration', '').strip()
        order_number = request.form.get('order_number', 0)
        module_id = request.form.get('module_id', type=int)
        
        if not all([course_id, title, video_url]):
            flash('Course, Title, and URL are required!', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if len(title) < 3 or len(title) > 100:
            flash('Video title must be between 3 and 100 characters.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if description and len(description) > 500:
            flash('Video description cannot exceed 500 characters.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if not (video_url.startswith('https://') and ('youtube.com' in video_url or 'youtu.be' in video_url or 'vimeo.com' in video_url)):
            flash('Video URL must be a valid YouTube or Vimeo HTTPS URL.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if duration and not duration.replace(':', '').isdigit():
            flash('Duration must use a time-like format such as 45:30.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        order_number_int = _parse_int(order_number, default=0, min_value=0)
        
        video = Video(
            course_id=course_id,
            title=title,
            video_url=video_url,
            description=description,
            duration=duration,
            module_id=module_id,
            order_number=order_number_int
        )
        db.session.add(video)
        db.session.commit()
        
        flash('Video added successfully!', 'success')
        return redirect(url_for('admin.manage_videos', course_id=course_id))
    except Exception as e:
        db.session.rollback()
        print(f"Error adding video: {e}")
        flash('Error adding video. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/video/<int:video_id>/update', methods=['POST'])
@admin_required
def update_video(video_id):
    """Update Video Information"""
    try:
        video = Video.query.get_or_404(video_id)
        course_id = video.course_id

        title = request.form.get('title', '').strip()
        video_url = request.form.get('video_url', '').strip()
        description = request.form.get('description', '').strip()
        duration = request.form.get('duration', '').strip()
        order_number = request.form.get('order_number', video.order_number)
        module_id = request.form.get('module_id', type=int)

        if not all([title, video_url]):
            flash('Video title and URL are required!', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if len(title) < 3 or len(title) > 100:
            flash('Video title must be between 3 and 100 characters.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if description and len(description) > 500:
            flash('Video description cannot exceed 500 characters.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if not (video_url.startswith('https://') and ('youtube.com' in video_url or 'youtu.be' in video_url or 'vimeo.com' in video_url)):
            flash('Video URL must be a valid YouTube or Vimeo HTTPS URL.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))
        if duration and not duration.replace(':', '').isdigit():
            flash('Duration must use a time-like format such as 45:30.', 'danger')
            return redirect(url_for('admin.manage_videos', course_id=course_id))

        video.title = title
        video.video_url = video_url
        video.description = description
        video.duration = duration
        video.module_id = module_id
        video.order_number = _parse_int(order_number, default=0, min_value=0)

        db.session.commit()
        flash('Video updated successfully!', 'success')
        return redirect(url_for('admin.manage_videos', course_id=course_id))
    except Exception as e:
        db.session.rollback()
        print(f"Error updating video: {e}")
        flash('Error updating video. Please try again.', 'danger')
        return redirect(url_for('admin.manage_courses'))

@admin_bp.route('/video/<int:video_id>/delete', methods=['POST'])
@admin_required
def delete_video(video_id):
    """Delete Video"""
    if not _require_destructive_confirmation():
        flash('Delete confirmation phrase required.', 'danger')
        video = Video.query.get_or_404(video_id)
        return redirect(url_for('admin.manage_videos', course_id=video.course_id))
    try:
        video = Video.query.get_or_404(video_id)
        course_id = video.course_id
        db.session.delete(video)
        db.session.commit()
        flash('Video deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting video: {e}")
        flash('Error deleting video. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_videos', course_id=course_id))

@admin_bp.route('/students')
@admin_required
def manage_students():
    """Manage Students"""
    try:
        page = _parse_int(request.args.get('page'), default=1)
        per_page = DEFAULT_PAGE_SIZE
        sort_key = request.args.get('sort', 'created_at').strip().lower()
        sort_dir = request.args.get('dir', 'desc').strip().lower()

        enrollment_counts = (
            db.session.query(
                Enrollment.user_id.label('user_id'),
                func.count(Enrollment.id).label('enrollment_count'),
            )
            .group_by(Enrollment.user_id)
            .subquery()
        )
        enrollment_count_col = func.coalesce(enrollment_counts.c.enrollment_count, 0)
        query = (
            db.session.query(User, enrollment_count_col.label('enrollment_count'))
            .outerjoin(enrollment_counts, enrollment_counts.c.user_id == User.id)
            .filter(User.role == 'student')
        )
        sort_columns = {
            'name': User.name,
            'email': User.email,
            'wallet_balance': User.wallet_balance,
            'enrollment_count': enrollment_count_col,
            'created_at': User.created_at,
        }
        if sort_key not in sort_columns:
            sort_key = 'created_at'
        if sort_dir not in {'asc', 'desc'}:
            sort_dir = 'desc'
        order_expr = sort_columns[sort_key].asc() if sort_dir == 'asc' else sort_columns[sort_key].desc()
        query = query.order_by(order_expr, User.id.desc())

        pagination = _paginate_query(query, page=page, per_page=per_page)
        return render_template(
            'admin/manage_students.html',
            student_rows=pagination['items'],
            pagination=pagination,
            sort=sort_key,
            direction=sort_dir,
        )
    except Exception as e:
        print(f"Error loading students: {e}")
        flash('Error loading students. Please try again.', 'danger')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/enrollments')
@admin_required
def view_enrollments():
    """View All Enrollments"""
    try:
        page = _parse_int(request.args.get('page'), default=1)
        per_page = DEFAULT_PAGE_SIZE
        sort_key = request.args.get('sort', 'enrolled_date').strip().lower()
        sort_dir = request.args.get('dir', 'desc').strip().lower()

        query = Enrollment.query.options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.course),
        )
        sort_columns = {
            'student': User.name,
            'course': Course.title,
            'enrolled_date': Enrollment.enrolled_date,
            'progress': Enrollment.progress,
            'status': Enrollment.completed,
        }
        if sort_key == 'student':
            query = query.join(User, Enrollment.user_id == User.id)
        elif sort_key == 'course':
            query = query.join(Course, Enrollment.course_id == Course.id)

        if sort_key not in sort_columns:
            sort_key = 'enrolled_date'
        if sort_dir not in {'asc', 'desc'}:
            sort_dir = 'desc'
        order_expr = sort_columns[sort_key].asc() if sort_dir == 'asc' else sort_columns[sort_key].desc()
        query = query.order_by(order_expr, Enrollment.id.desc())

        pagination = _paginate_query(query, page=page, per_page=per_page)
        return render_template(
            'admin/view_enrollments.html',
            enrollments=pagination['items'],
            pagination=pagination,
            sort=sort_key,
            direction=sort_dir,
        )
    except Exception as e:
        print(f"Error loading enrollments: {e}")
        flash('Error loading enrollments. Please try again.', 'danger')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/enrolls')
@admin_required
def view_enrollments_alias():
    """Legacy alias for enrollment list."""
    return redirect(url_for('admin.view_enrollments'))

@admin_bp.route('/referrals')
@admin_required
def view_referrals():
    """View Referral Transactions"""
    try:
        page = _parse_int(request.args.get('page'), default=1)
        per_page = DEFAULT_PAGE_SIZE
        sort_key = request.args.get('sort', 'date').strip().lower()
        sort_dir = request.args.get('dir', 'desc').strip().lower()

        query = ReferralTransaction.query.options(
            joinedload(ReferralTransaction.referrer),
            joinedload(ReferralTransaction.new_user),
        )
        sort_columns = {
            'date': ReferralTransaction.date,
            'reward_amount': ReferralTransaction.reward_amount,
            'status': ReferralTransaction.status,
        }
        if sort_key not in sort_columns:
            sort_key = 'date'
        if sort_dir not in {'asc', 'desc'}:
            sort_dir = 'desc'
        order_expr = sort_columns[sort_key].asc() if sort_dir == 'asc' else sort_columns[sort_key].desc()
        query = query.order_by(order_expr, ReferralTransaction.id.desc())

        pagination = _paginate_query(query, page=page, per_page=per_page)
        total_referrals = db.session.query(func.count(ReferralTransaction.id)).scalar() or 0
        total_spent = db.session.query(func.coalesce(func.sum(ReferralTransaction.reward_amount), 0)).scalar() or 0
        
        return render_template('admin/view_referrals.html', 
                             referrals=pagination['items'],
                             pagination=pagination,
                             sort=sort_key,
                             direction=sort_dir,
                             total_referrals=total_referrals,
                             total_spent=total_spent)
    except Exception as e:
        print(f"Error loading referrals: {e}")
        flash('Error loading referrals. Please try again.', 'danger')
        return redirect(url_for('admin.dashboard'))


# ============================================
# ADMIN MANAGEMENT ROUTES
# ============================================

@admin_bp.route('/admins')
@admin_required
def manage_admins():
    """Manage Admin Users"""
    try:
        admin_users = AdminUser.query.all()
        return render_template('admin/manage_admins.html', admin_users=admin_users, admin_roles=ADMIN_ROLES)
    except Exception as e:
        print(f"Error loading admins: {e}")
        flash('Error loading admins. Please try again.', 'danger')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/admin/add', methods=['POST'])
@admin_required
def add_admin():
    """Add New Admin"""
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        admin_role = (request.form.get('admin_role') or 'content_admin').strip().lower()
        
        if not all([username, password]):
            flash('Username and password are required!', 'danger')
            return redirect(url_for('admin.manage_admins'))
        is_strong, message = _validate_admin_password_strength(password)
        if not is_strong:
            flash(message, 'danger')
            return redirect(url_for('admin.manage_admins'))
        if admin_role not in ADMIN_ROLES:
            flash('Invalid admin role selected.', 'danger')
            return redirect(url_for('admin.manage_admins'))
        
        # Check if username already exists
        if AdminUser.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('admin.manage_admins'))
        
        # Create admin user in User table
        user = User(name=full_name or username, email=email or f'{username}@admin.local', role='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Get the user ID
        user.referral_code = user.generate_referral_code()
        
        # Create admin profile
        admin_user = AdminUser(
            user_id=user.id,
            username=username,
            full_name=full_name,
            email=email,
            role=admin_role,
            password_changed_at=datetime.utcnow(),
        )
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
        log_audit(
            entity_type='admin_user',
            entity_id=admin_user.id,
            action_type='create_admin',
            after={'username': admin_user.username, 'role': admin_user.role, 'user_id': admin_user.user_id},
        )
        
        flash(f'Admin "{username}" added successfully!', 'success')
        return redirect(url_for('admin.manage_admins'))
    except Exception as e:
        db.session.rollback()
        print(f"Error adding admin: {e}")
        flash('Error adding admin. Please try again.', 'danger')
        return redirect(url_for('admin.manage_admins'))


@admin_bp.route('/admin/<int:admin_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_admin(admin_id):
    """Edit Admin Credentials"""
    admin_user = AdminUser.query.get_or_404(admin_id)
    
    if request.method == 'POST':
        try:
            before_values = {
                'username': admin_user.username,
                'full_name': admin_user.full_name,
                'email': admin_user.email,
                'role': admin_user.role,
            }
            # Update username
            new_username = request.form.get('username', '').strip()
            if new_username and new_username != admin_user.username:
                if AdminUser.query.filter_by(username=new_username).first():
                    flash('Username already exists!', 'danger')
                    return redirect(url_for('admin.edit_admin', admin_id=admin_id))
                admin_user.username = new_username
            
            # Update password if provided
            new_password = request.form.get('password', '').strip()
            if new_password:
                is_strong, message = _validate_admin_password_strength(new_password)
                if not is_strong:
                    flash(message, 'danger')
                    return redirect(url_for('admin.edit_admin', admin_id=admin_id))
                admin_user.set_password(new_password)
                admin_user.password_changed_at = datetime.utcnow()
            
            # Update other info
            admin_user.full_name = request.form.get('full_name', '').strip()
            admin_user.email = request.form.get('email', '').strip()
            requested_role = (request.form.get('admin_role') or admin_user.role or 'content_admin').strip().lower()
            if requested_role not in ADMIN_ROLES:
                flash('Invalid admin role selected.', 'danger')
                return redirect(url_for('admin.edit_admin', admin_id=admin_id))
            admin_user.role = requested_role
            
            # Also update the User table
            user = admin_user.user
            user.name = admin_user.full_name or admin_user.username
            user.email = admin_user.email or user.email
            
            db.session.commit()
            after_values = {
                'username': admin_user.username,
                'full_name': admin_user.full_name,
                'email': admin_user.email,
                'role': admin_user.role,
            }
            action_type = 'update_admin'
            if before_values.get('role') != after_values.get('role'):
                action_type = 'admin_role_change'
            log_audit(
                entity_type='admin_user',
                entity_id=admin_user.id,
                action_type=action_type,
                before=before_values,
                after=after_values,
            )
            if session.get('user_id') == admin_user.user_id:
                session['admin_role'] = admin_user.role
            flash('Admin updated successfully!', 'success')
            return redirect(url_for('admin.manage_admins'))
        except Exception as e:
            db.session.rollback()
            print(f"Error editing admin: {e}")
            flash('Error updating admin. Please try again.', 'danger')
    
    return render_template('admin/edit_admin.html', admin_user=admin_user, admin_roles=ADMIN_ROLES)


@admin_bp.route('/admin/<int:admin_id>/delete', methods=['POST'])
@admin_required
def delete_admin(admin_id):
    """Delete Admin"""
    if not _require_destructive_confirmation():
        flash('Delete confirmation phrase required.', 'danger')
        return redirect(url_for('admin.manage_admins'))
    try:
        # Prevent deleting the last admin
        admin_count = AdminUser.query.count()
        if admin_count <= 1:
            flash('Cannot delete the last admin user!', 'danger')
            return redirect(url_for('admin.manage_admins'))
        
        admin_user = AdminUser.query.get_or_404(admin_id)
        before_values = {
            'username': admin_user.username,
            'role': admin_user.role,
            'user_id': admin_user.user_id,
        }
        username = admin_user.username
        user_id = admin_user.user_id
        
        # Delete admin profile
        db.session.delete(admin_user)
        
        # Optionally delete from User table too
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
        
        db.session.commit()
        log_audit(
            entity_type='admin_user',
            entity_id=admin_id,
            action_type='delete_admin',
            before=before_values,
            after=None,
        )
        flash(f'Admin "{username}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting admin: {e}")
        flash('Error deleting admin. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_admins'))
