from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Course, Enrollment, Quiz, QuizQuestion, QuizAttempt, QuizAnswer
from student_routes import student_required
from datetime import datetime, timedelta
from sqlalchemy import func
from learning_utils import update_learning_streak, refresh_progress_on_quiz_completion

student_quiz_bp = Blueprint('student_quiz', __name__, url_prefix='/student')


def _current_student():
    return User.query.get(session.get('user_id'))


def _ensure_enrolled(user_id, course_id):
    return Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first() is not None


def _quiz_attempt_session_key(quiz_id):
    return f'active_quiz_attempt_{quiz_id}'


def _ordered_questions_query(quiz_id):
    return (
        QuizQuestion.query
        .filter_by(quiz_id=quiz_id)
        .order_by(func.coalesce(QuizQuestion.order_index, QuizQuestion.order_number).asc(), QuizQuestion.id.asc())
    )


@student_quiz_bp.route('/course/<int:course_id>/quizzes')
@student_required
def course_quizzes(course_id):
    user = _current_student()
    course = Course.query.get_or_404(course_id)
    if not _ensure_enrolled(user.id, course.id):
        flash('Please enroll in this course to access quizzes.', 'warning')
        return redirect(url_for('student.course_details', course_id=course.id))

    quizzes = Quiz.query.filter_by(course_id=course.id, is_enabled=True).order_by(Quiz.created_at.asc()).all()
    attempt_counts = {
        row[0]: row[1]
        for row in db.session.query(QuizAttempt.quiz_id, db.func.count(QuizAttempt.id))
        .filter(QuizAttempt.user_id == user.id)
        .group_by(QuizAttempt.quiz_id)
        .all()
    }
    return render_template(
        'student/quizzes/course_quizzes.html',
        course=course,
        quizzes=quizzes,
        attempt_counts=attempt_counts,
    )


@student_quiz_bp.route('/quiz/<int:quiz_id>')
@student_required
def take_quiz(quiz_id):
    user = _current_student()
    quiz = Quiz.query.get_or_404(quiz_id)
    if not quiz.is_enabled:
        flash('This quiz is currently disabled.', 'warning')
        return redirect(url_for('student_quiz.course_quizzes', course_id=quiz.course_id))
    if not _ensure_enrolled(user.id, quiz.course_id):
        flash('Please enroll in this course first.', 'warning')
        return redirect(url_for('student.course_details', course_id=quiz.course_id))

    attempts_used = QuizAttempt.query.filter_by(user_id=user.id, quiz_id=quiz.id).count()

    questions = _ordered_questions_query(quiz.id).all()
    if not questions:
        flash('Quiz has no questions yet.', 'warning')
        return redirect(url_for('student_quiz.course_quizzes', course_id=quiz.course_id))

    now = datetime.utcnow()
    active_attempt = None
    active_attempt_id = session.get(_quiz_attempt_session_key(quiz.id))
    if active_attempt_id:
        active_attempt = QuizAttempt.query.filter_by(
            id=active_attempt_id,
            user_id=user.id,
            quiz_id=quiz.id,
        ).first()
        if not active_attempt or active_attempt.submitted_at is not None:
            active_attempt = None
            session.pop(_quiz_attempt_session_key(quiz.id), None)

    if active_attempt is None and attempts_used >= quiz.attempts_allowed:
        flash('You have reached the maximum attempts for this quiz.', 'warning')
        return redirect(url_for('student_quiz.course_quizzes', course_id=quiz.course_id))

    if active_attempt is None:
        active_attempt = QuizAttempt.query.filter_by(
            user_id=user.id,
            quiz_id=quiz.id,
            submitted_at=None,
        ).order_by(QuizAttempt.id.desc()).first()

    if active_attempt and active_attempt.end_time and now > active_attempt.end_time:
        active_attempt.submitted_at = now
        active_attempt.started_at = active_attempt.start_time or active_attempt.started_at or now
        active_attempt.total_questions = len(questions)
        active_attempt.correct_answers = 0
        active_attempt.score_percentage = 0.0
        active_attempt.passed = False
        db.session.commit()
        active_attempt = None
        session.pop(_quiz_attempt_session_key(quiz.id), None)
        flash('Previous timed attempt expired and was auto-submitted.', 'warning')

    if active_attempt is None:
        start_time = now
        end_time = now + timedelta(minutes=max(1, int(quiz.time_limit_minutes or 15)))
        active_attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=user.id,
            attempt_number=attempts_used + 1,
            total_questions=len(questions),
            correct_answers=0,
            score_percentage=0.0,
            passed=False,
            start_time=start_time,
            end_time=end_time,
            started_at=start_time,
            submitted_at=None,
        )
        db.session.add(active_attempt)
        db.session.commit()

    session[_quiz_attempt_session_key(quiz.id)] = active_attempt.id
    remaining_seconds = 0
    if active_attempt.end_time:
        remaining_seconds = max(0, int((active_attempt.end_time - datetime.utcnow()).total_seconds()))
    return render_template(
        'student/quizzes/take_quiz.html',
        quiz=quiz,
        questions=questions,
        attempts_used=attempts_used,
        active_attempt=active_attempt,
        remaining_seconds=remaining_seconds,
    )


@student_quiz_bp.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@student_required
def submit_quiz(quiz_id):
    user = _current_student()
    quiz = Quiz.query.get_or_404(quiz_id)
    if not _ensure_enrolled(user.id, quiz.course_id):
        flash('Please enroll in this course first.', 'warning')
        return redirect(url_for('student.course_details', course_id=quiz.course_id))

    questions = _ordered_questions_query(quiz.id).all()
    if not questions:
        flash('Quiz has no questions yet.', 'warning')
        return redirect(url_for('student_quiz.course_quizzes', course_id=quiz.course_id))

    attempt_id = request.form.get('attempt_id', type=int) or session.get(_quiz_attempt_session_key(quiz.id))
    if not attempt_id:
        flash('Quiz attempt session expired. Please start again.', 'warning')
        return redirect(url_for('student_quiz.take_quiz', quiz_id=quiz.id))
    attempt = QuizAttempt.query.filter_by(
        id=attempt_id,
        user_id=user.id,
        quiz_id=quiz.id,
    ).first()
    if not attempt or attempt.submitted_at is not None:
        flash('This quiz attempt has already been submitted.', 'warning')
        return redirect(url_for('student_quiz.course_quizzes', course_id=quiz.course_id))

    now = datetime.utcnow()
    timed_out = bool(attempt.end_time and now > attempt.end_time)

    correct_count = 0
    answers_payload = []
    for question in questions:
        field_name = f'question_{question.id}'
        submitted_answer = (request.form.get(field_name) or '').strip()
        expected = (question.correct_answer or '').strip()
        if question.question_type == 'mcq':
            is_correct = submitted_answer.upper() == expected.upper()
        elif question.question_type == 'true_false':
            is_correct = submitted_answer.lower() == expected.lower()
        else:
            is_correct = submitted_answer.lower() == expected.lower()
        if is_correct:
            correct_count += 1
        answers_payload.append((question.id, submitted_answer, is_correct))

    total_questions = len(questions)
    score_percentage = round((correct_count / total_questions) * 100, 2) if total_questions else 0
    passed = score_percentage >= quiz.passing_percentage
    attempt.started_at = attempt.start_time or attempt.started_at or now
    attempt.submitted_at = now
    attempt.total_questions = total_questions
    attempt.correct_answers = correct_count
    attempt.score_percentage = score_percentage
    attempt.passed = passed
    try:
        existing_answers = QuizAnswer.query.filter_by(attempt_id=attempt.id).all()
        for old_answer in existing_answers:
            db.session.delete(old_answer)
        for question_id, submitted_answer, is_correct in answers_payload:
            db.session.add(QuizAnswer(
                attempt_id=attempt.id,
                question_id=question_id,
                submitted_answer=submitted_answer,
                is_correct=is_correct,
            ))
        update_learning_streak(user.id)
        refresh_progress_on_quiz_completion(user.id, quiz.course_id)
        db.session.commit()
        session.pop(_quiz_attempt_session_key(quiz.id), None)
        if timed_out:
            flash('Time limit reached. Quiz was auto-submitted.', 'warning')
        return redirect(url_for('student_quiz.quiz_result', attempt_id=attempt.id))
    except Exception as e:
        db.session.rollback()
        print(f'Error submitting quiz: {e}')
        flash('Could not submit quiz. Please try again.', 'danger')
        return redirect(url_for('student_quiz.take_quiz', quiz_id=quiz.id))


@student_quiz_bp.route('/quiz-attempt/<int:attempt_id>/result')
@student_required
def quiz_result(attempt_id):
    user = _current_student()
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    if attempt.user_id != user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('student.dashboard'))
    quiz = attempt.quiz
    return render_template('student/quizzes/quiz_result.html', attempt=attempt, quiz=quiz)
