from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Course, Enrollment, Assignment, AssignmentSubmission
from student_routes import student_required
from learning_utils import update_learning_streak, refresh_progress_on_assignment_submission
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

student_assignment_bp = Blueprint('student_assignment', __name__, url_prefix='/student')

SUBMISSION_UPLOAD_DIR = os.path.join('uploads', 'assignments')
ALLOWED_SUBMISSION_EXTENSIONS = {'.pdf', '.docx', '.txt', '.zip'}


def _current_student():
    return User.query.get(session.get('user_id'))


def _ensure_enrolled(user_id, course_id):
    return Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first() is not None


def _save_submission_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    os.makedirs(SUBMISSION_UPLOAD_DIR, exist_ok=True)
    filename = secure_filename(file_storage.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_SUBMISSION_EXTENSIONS:
        return False
    unique_name = f"{uuid.uuid4().hex[:10]}_{filename}"
    out_path = os.path.join(SUBMISSION_UPLOAD_DIR, unique_name)
    file_storage.save(out_path)
    return out_path.replace('\\', '/')


@student_assignment_bp.route('/course/<int:course_id>/assignments')
@student_required
def course_assignments(course_id):
    user = _current_student()
    course = Course.query.get_or_404(course_id)
    if not _ensure_enrolled(user.id, course.id):
        flash('Please enroll in this course to access assignments.', 'warning')
        return redirect(url_for('student.course_details', course_id=course.id))

    assignments = Assignment.query.filter_by(course_id=course.id).order_by(Assignment.created_at.desc()).all()
    submissions = AssignmentSubmission.query.filter_by(user_id=user.id).all()
    submission_map = {submission.assignment_id: submission for submission in submissions}
    return render_template(
        'student/assignments/course_assignments.html',
        course=course,
        assignments=assignments,
        submission_map=submission_map,
    )


@student_assignment_bp.route('/assignment/<int:assignment_id>/submit', methods=['POST'])
@student_required
def submit_assignment(assignment_id):
    user = _current_student()
    assignment = Assignment.query.get_or_404(assignment_id)
    if not _ensure_enrolled(user.id, assignment.course_id):
        flash('Please enroll in this course first.', 'warning')
        return redirect(url_for('student.course_details', course_id=assignment.course_id))

    answer_text = request.form.get('answer_text', '').strip()
    submission_file = _save_submission_file(request.files.get('submission_file'))
    if submission_file is False:
        flash('Unsupported file type. Allowed: PDF, DOCX, TXT, ZIP.', 'danger')
        return redirect(url_for('student_assignment.course_assignments', course_id=assignment.course_id))
    if not answer_text and not submission_file:
        flash('Please provide text answer or upload a file.', 'danger')
        return redirect(url_for('student_assignment.course_assignments', course_id=assignment.course_id))

    existing = AssignmentSubmission.query.filter_by(user_id=user.id, assignment_id=assignment.id).first()
    try:
        if existing:
            existing.answer_text = answer_text
            if submission_file:
                existing.submission_file = submission_file
            existing.submitted_at = datetime.utcnow()
            existing.marks_awarded = None
            existing.feedback = None
            existing.graded_at = None
        else:
            db.session.add(AssignmentSubmission(
                assignment_id=assignment.id,
                user_id=user.id,
                answer_text=answer_text,
                submission_file=submission_file,
                submitted_at=datetime.utcnow(),
            ))
        update_learning_streak(user.id)
        refresh_progress_on_assignment_submission(user.id, assignment.course_id)
        db.session.commit()
        flash('Assignment submitted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error submitting assignment: {e}')
        flash('Could not submit assignment.', 'danger')
    return redirect(url_for('student_assignment.course_assignments', course_id=assignment.course_id))
