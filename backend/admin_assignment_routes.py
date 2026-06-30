from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.models import db, Course, Assignment, AssignmentSubmission, CourseModule
from backend.admin_routes import admin_required, ADMIN_ROLE_PERMISSIONS
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
import os
import uuid

admin_assignment_bp = Blueprint('admin_assignment', __name__, url_prefix='/admin')

ASSIGNMENT_UPLOAD_DIR = os.path.join('uploads', 'assignments')
SUBMISSION_UPLOAD_DIR = os.path.join('uploads', 'submissions')
ALLOWED_DOC_EXT = {'.pdf', '.docx', '.txt', '.zip'}


@admin_assignment_bp.before_request
def enforce_assignment_admin_security():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Please login as admin.', 'warning')
        return redirect(url_for('auth.login'))
    endpoint = (request.endpoint or '').split('.')[-1]
    role = (session.get('admin_role') or 'super_admin').strip().lower()
    allowed = ADMIN_ROLE_PERMISSIONS.get(role, set())
    if '*' not in allowed and endpoint not in allowed:
        flash('Access denied for your admin role.', 'danger')
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        token = session.get('csrf_token')
        request_token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
        if token and request_token != token:
            flash('Invalid CSRF token.', 'danger')
            return redirect(request.referrer or url_for('admin.dashboard'))


def _ensure_upload_dirs():
    os.makedirs(ASSIGNMENT_UPLOAD_DIR, exist_ok=True)
    os.makedirs(SUBMISSION_UPLOAD_DIR, exist_ok=True)


def _save_upload(file_storage, folder):
    if not file_storage or not file_storage.filename:
        return None
    filename = secure_filename(file_storage.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_DOC_EXT:
        return None
    unique = f"{uuid.uuid4().hex[:10]}_{filename}"
    path = os.path.join(folder, unique)
    file_storage.save(path)
    return path.replace('\\', '/')


@admin_assignment_bp.route('/assignments')
@admin_required
def assignments_overview():
    courses = Course.query.order_by(Course.title.asc()).all()
    return render_template('admin/assignments/index.html', courses=courses)


@admin_assignment_bp.route('/course/<int:course_id>/assignments')
@admin_required
def manage_course_assignments(course_id):
    course = Course.query.get_or_404(course_id)
    page = request.args.get('page', 1, type=int)
    assignments = (
        Assignment.query
        .filter_by(course_id=course.id)
        .order_by(Assignment.created_at.desc())
        .paginate(page=page, per_page=20, error_out=False)
    )
    modules = CourseModule.query.filter_by(course_id=course.id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()
    return render_template('admin/assignments/manage_assignments.html', course=course, assignments=assignments, modules=modules)


@admin_assignment_bp.route('/course/<int:course_id>/assignments/add', methods=['POST'])
@admin_required
def add_assignment(course_id):
    course = Course.query.get_or_404(course_id)
    _ensure_upload_dirs()
    title = request.form.get('title', '').strip()
    instructions = request.form.get('instructions', '').strip()
    due_date_raw = request.form.get('due_date', '').strip()
    marks_raw = request.form.get('marks', '100').strip()

    if not title or not instructions:
        flash('Assignment title and instructions are required.', 'danger')
        return redirect(url_for('admin_assignment.manage_course_assignments', course_id=course.id))
    try:
        due_date = datetime.fromisoformat(due_date_raw) if due_date_raw else None
        marks = max(1, float(marks_raw or 100))
        attachment_file = request.files.get('attachment')
        attachment = _save_upload(attachment_file, ASSIGNMENT_UPLOAD_DIR)
        if attachment_file and attachment_file.filename and not attachment:
            flash('Unsupported file type. Allowed: PDF, DOCX, TXT, ZIP.', 'danger')
            return redirect(url_for('admin_assignment.manage_course_assignments', course_id=course.id))
        assignment = Assignment(
            course_id=course.id,
            title=title,
            instructions=instructions,
            due_date=due_date,
            marks=marks,
            module_id=request.form.get('module_id', type=int),
            attachment_path=attachment,
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error creating assignment: {e}')
        flash('Could not create assignment.', 'danger')
    return redirect(url_for('admin_assignment.manage_course_assignments', course_id=course.id))


@admin_assignment_bp.route('/assignment/<int:assignment_id>/edit', methods=['POST'])
@admin_required
def edit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    _ensure_upload_dirs()
    try:
        assignment.title = request.form.get('title', assignment.title).strip() or assignment.title
        assignment.instructions = request.form.get('instructions', assignment.instructions).strip() or assignment.instructions
        due_date_raw = request.form.get('due_date', '').strip()
        assignment.due_date = datetime.fromisoformat(due_date_raw) if due_date_raw else None
        assignment.marks = max(1, float(request.form.get('marks', assignment.marks)))
        assignment.module_id = request.form.get('module_id', type=int)
        attachment_file = request.files.get('attachment')
        new_attachment = _save_upload(attachment_file, ASSIGNMENT_UPLOAD_DIR)
        if attachment_file and attachment_file.filename and not new_attachment:
            flash('Unsupported file type. Allowed: PDF, DOCX, TXT, ZIP.', 'danger')
            return redirect(url_for('admin_assignment.manage_course_assignments', course_id=assignment.course_id))
        if new_attachment:
            assignment.attachment_path = new_attachment
        db.session.commit()
        flash('Assignment updated.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error updating assignment: {e}')
        flash('Could not update assignment.', 'danger')
    return redirect(url_for('admin_assignment.manage_course_assignments', course_id=assignment.course_id))


@admin_assignment_bp.route('/assignment/<int:assignment_id>/delete', methods=['POST'])
@admin_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course_id = assignment.course_id
    try:
        db.session.delete(assignment)
        db.session.commit()
        flash('Assignment deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error deleting assignment: {e}')
        flash('Could not delete assignment.', 'danger')
    return redirect(url_for('admin_assignment.manage_course_assignments', course_id=course_id))


@admin_assignment_bp.route('/assignment/<int:assignment_id>/submissions')
@admin_required
def assignment_submissions(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    page = request.args.get('page', 1, type=int)
    submissions = (
        AssignmentSubmission.query
        .filter_by(assignment_id=assignment.id)
        .order_by(AssignmentSubmission.submitted_at.desc())
        .paginate(page=page, per_page=20, error_out=False)
    )
    return render_template('admin/assignments/submissions.html', assignment=assignment, submissions=submissions)


@admin_assignment_bp.route('/submission/<int:submission_id>/grade', methods=['POST'])
@admin_required
def grade_submission(submission_id):
    submission = AssignmentSubmission.query.get_or_404(submission_id)
    try:
        marks_awarded_raw = request.form.get('marks_awarded', '').strip()
        feedback = request.form.get('feedback', '').strip()
        if marks_awarded_raw:
            submission.marks_awarded = float(marks_awarded_raw)
        submission.feedback = feedback
        submission.graded_at = datetime.utcnow()
        db.session.commit()
        flash('Submission graded successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error grading submission: {e}')
        flash('Could not grade submission.', 'danger')
    return redirect(url_for('admin_assignment.assignment_submissions', assignment_id=submission.assignment_id))
