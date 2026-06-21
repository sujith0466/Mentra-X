from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from backend.models import db, Course, Quiz, QuizQuestion, CourseModule, Video
from backend.admin_routes import admin_required, ADMIN_ROLE_PERMISSIONS
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os
import re
import tempfile

admin_quiz_bp = Blueprint('admin_quiz', __name__, url_prefix='/admin')

ALLOWED_IMPORT_EXTENSIONS = {'.txt', '.pdf', '.docx'}


@admin_quiz_bp.before_request
def enforce_quiz_admin_security():
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


def _quiz_course(course_id):
    return Course.query.get_or_404(course_id)


def _normalize_question_type(raw_type):
    allowed = {'mcq', 'true_false', 'short_answer', 'long_answer'}
    value = (raw_type or 'mcq').strip().lower()
    return value if value in allowed else 'mcq'


def _next_question_order(quiz_id):
    current_max = (
        db.session.query(func.max(func.coalesce(QuizQuestion.order_index, QuizQuestion.order_number)))
        .filter(QuizQuestion.quiz_id == quiz_id)
        .scalar()
    )
    return int(current_max or 0) + 1


def _parse_question_blocks(raw_text):
    """
    Parse formatted quiz text blocks:
    1. Question
       A. ...
       B. ...
       C. ...
       D. ...
       Answer: A
    """
    parsed_questions = []
    if not raw_text:
        return parsed_questions

    lines = [line.rstrip() for line in raw_text.splitlines() if line.strip()]
    blocks = []
    current = []
    for line in lines:
        if re.match(r'^\d+[\.\)]\s+', line.strip()) and current:
            blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append(current)

    for block in blocks:
        question_text = ''
        options = {}
        answer_value = ''

        for idx, line in enumerate(block):
            stripped = line.strip()
            if idx == 0:
                question_text = re.sub(r'^\d+[\.\)]\s*', '', stripped).strip()
                continue
            option_match = re.match(r'^([A-D])[\.\)]\s*(.+)$', stripped, re.IGNORECASE)
            if option_match:
                options[option_match.group(1).upper()] = option_match.group(2).strip()
                continue
            answer_match = re.match(r'^Answer\s*:\s*(.+)$', stripped, re.IGNORECASE)
            if answer_match:
                answer_value = answer_match.group(1).strip()

        if not question_text:
            continue

        if options:
            answer_key = answer_value.upper()[:1]
            parsed_questions.append({
                'question_text': question_text,
                'question_type': 'mcq',
                'option_a': options.get('A', ''),
                'option_b': options.get('B', ''),
                'option_c': options.get('C', ''),
                'option_d': options.get('D', ''),
                'correct_answer': answer_key if answer_key in {'A', 'B', 'C', 'D'} else 'A',
            })
        else:
            answer_norm = (answer_value or '').strip()
            lower_answer = answer_norm.lower()
            if lower_answer in {'true', 'false'}:
                q_type = 'true_false'
            elif len(answer_norm) > 140:
                q_type = 'long_answer'
            else:
                q_type = 'short_answer'
            parsed_questions.append({
                'question_text': question_text,
                'question_type': q_type,
                'correct_answer': answer_norm or 'N/A',
                'option_a': None,
                'option_b': None,
                'option_c': None,
                'option_d': None,
            })
    return parsed_questions


def _extract_text_from_upload(file_storage):
    filename = secure_filename(file_storage.filename or '')
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_IMPORT_EXTENSIONS:
        raise ValueError('Unsupported file type. Use TXT, PDF, or DOCX.')

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file_storage.save(tmp.name)
        tmp_path = tmp.name
    try:
        if ext == '.txt':
            with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as fp:
                return fp.read()
        if ext == '.pdf':
            try:
                from PyPDF2 import PdfReader
            except Exception as exc:
                raise ValueError('PDF parsing requires PyPDF2 package.') from exc
            reader = PdfReader(tmp_path)
            return '\n'.join((page.extract_text() or '') for page in reader.pages)
        if ext == '.docx':
            try:
                import docx
            except Exception as exc:
                raise ValueError('DOCX parsing requires python-docx package.') from exc
            doc = docx.Document(tmp_path)
            return '\n'.join(p.text for p in doc.paragraphs)
        return ''
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


@admin_quiz_bp.route('/quizzes')
@admin_required
def quizzes_overview():
    courses = Course.query.order_by(Course.title.asc()).all()
    return render_template('admin/quizzes/index.html', courses=courses)


@admin_quiz_bp.route('/course/<int:course_id>/quizzes')
@admin_required
def manage_course_quizzes(course_id):
    course = _quiz_course(course_id)
    page = request.args.get('page', 1, type=int)
    quizzes = (
        Quiz.query
        .filter_by(course_id=course.id)
        .order_by(Quiz.created_at.desc())
        .paginate(page=page, per_page=20, error_out=False)
    )
    modules = CourseModule.query.filter_by(course_id=course.id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()
    return render_template('admin/quizzes/manage_quizzes.html', course=course, quizzes=quizzes, modules=modules)


@admin_quiz_bp.route('/course/<int:course_id>/quizzes/add', methods=['POST'])
@admin_required
def add_quiz(course_id):
    course = _quiz_course(course_id)
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    passing_percentage = request.form.get('passing_percentage', '60').strip()
    time_limit_minutes = request.form.get('time_limit_minutes', '15').strip()
    attempts_allowed = request.form.get('attempts_allowed', '3').strip()
    question_count_target = request.form.get('question_count_target', '10').strip()
    is_enabled = request.form.get('is_enabled') == 'on'

    if not title:
        flash('Quiz title is required.', 'danger')
        return redirect(url_for('admin_quiz.manage_course_quizzes', course_id=course.id))
    try:
        quiz = Quiz(
            course_id=course.id,
            title=title,
            description=description,
            question_count_target=max(1, int(question_count_target or 10)),
            passing_percentage=max(0, min(100, float(passing_percentage or 60))),
            time_limit_minutes=max(1, int(time_limit_minutes or 15)),
            attempts_allowed=max(1, int(attempts_allowed or 3)),
            module_id=request.form.get('module_id', type=int),
            is_enabled=is_enabled,
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error adding quiz: {e}')
        flash('Could not create quiz.', 'danger')
    return redirect(url_for('admin_quiz.manage_course_quizzes', course_id=course.id))


@admin_quiz_bp.route('/quiz/<int:quiz_id>/edit', methods=['POST'])
@admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    try:
        quiz.title = request.form.get('title', quiz.title).strip() or quiz.title
        quiz.description = request.form.get('description', quiz.description or '').strip()
        quiz.question_count_target = max(1, int(request.form.get('question_count_target', quiz.question_count_target)))
        quiz.passing_percentage = max(0, min(100, float(request.form.get('passing_percentage', quiz.passing_percentage))))
        quiz.time_limit_minutes = max(1, int(request.form.get('time_limit_minutes', quiz.time_limit_minutes)))
        quiz.attempts_allowed = max(1, int(request.form.get('attempts_allowed', quiz.attempts_allowed)))
        quiz.module_id = request.form.get('module_id', type=int)
        quiz.is_enabled = request.form.get('is_enabled') == 'on'
        db.session.commit()
        flash('Quiz updated.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error updating quiz: {e}')
        flash('Could not update quiz.', 'danger')
    return redirect(url_for('admin_quiz.manage_course_quizzes', course_id=quiz.course_id))


@admin_quiz_bp.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    course_id = quiz.course_id
    try:
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error deleting quiz: {e}')
        flash('Could not delete quiz.', 'danger')
    return redirect(url_for('admin_quiz.manage_course_quizzes', course_id=course_id))


@admin_quiz_bp.route('/quiz/<int:quiz_id>/questions')
@admin_required
def manage_quiz_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    page = request.args.get('page', 1, type=int)
    questions = (
        QuizQuestion.query
        .filter_by(quiz_id=quiz.id)
        .order_by(func.coalesce(QuizQuestion.order_index, QuizQuestion.order_number).asc(), QuizQuestion.id.asc())
        .paginate(page=page, per_page=20, error_out=False)
    )
    lessons = Video.query.filter_by(course_id=quiz.course_id).order_by(Video.order_number.asc(), Video.id.asc()).all()
    return render_template('admin/quizzes/manage_questions.html', quiz=quiz, questions=questions, lessons=lessons)


@admin_quiz_bp.route('/quiz/<int:quiz_id>/questions/add', methods=['POST'])
@admin_required
def add_quiz_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    try:
        question_type = _normalize_question_type(request.form.get('question_type'))
        order_index = request.form.get('order_index', type=int) or _next_question_order(quiz.id)
        question = QuizQuestion(
            quiz_id=quiz.id,
            question_text=request.form.get('question_text', '').strip(),
            question_type=question_type,
            option_a=request.form.get('option_a', '').strip() or None,
            option_b=request.form.get('option_b', '').strip() or None,
            option_c=request.form.get('option_c', '').strip() or None,
            option_d=request.form.get('option_d', '').strip() or None,
            correct_answer=request.form.get('correct_answer', '').strip(),
            order_index=order_index,
            order_number=order_index,
        )
        if not question.question_text or not question.correct_answer:
            flash('Question text and correct answer are required.', 'danger')
            return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))
        db.session.add(question)
        db.session.commit()
        flash('Question added.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error adding question: {e}')
        flash('Could not add question.', 'danger')
    return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))


@admin_quiz_bp.route('/question/<int:question_id>/edit', methods=['POST'])
@admin_required
def edit_quiz_question(question_id):
    question = QuizQuestion.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    try:
        question.question_text = request.form.get('question_text', question.question_text).strip()
        question.question_type = _normalize_question_type(request.form.get('question_type', question.question_type))
        question.option_a = request.form.get('option_a', '').strip() or None
        question.option_b = request.form.get('option_b', '').strip() or None
        question.option_c = request.form.get('option_c', '').strip() or None
        question.option_d = request.form.get('option_d', '').strip() or None
        question.correct_answer = request.form.get('correct_answer', question.correct_answer).strip()
        order_index = request.form.get('order_index', type=int)
        if order_index is not None and order_index > 0:
            question.order_index = order_index
            question.order_number = order_index
        db.session.commit()
        flash('Question updated.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error editing question: {e}')
        flash('Could not update question.', 'danger')
    return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz_id))


@admin_quiz_bp.route('/question/<int:question_id>/delete', methods=['POST'])
@admin_required
def delete_quiz_question(question_id):
    question = QuizQuestion.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    try:
        db.session.delete(question)
        db.session.commit()
        flash('Question deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error deleting question: {e}')
        flash('Could not delete question.', 'danger')
    return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz_id))


@admin_quiz_bp.route('/quiz/<int:quiz_id>/questions/reorder', methods=['POST'])
@admin_required
def reorder_quiz_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json(silent=True) or {}
    ordered_ids = data.get('ordered_ids') or []
    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
    valid_ids = {q.id for q in questions}
    if not ordered_ids or not set(ordered_ids).issubset(valid_ids):
        return jsonify({'success': False, 'error': 'Invalid question ids'}), 400
    try:
        question_map = {q.id: q for q in questions}
        current_pos = {
            q.id: idx
            for idx, q in enumerate(
                sorted(questions, key=lambda item: ((item.order_index or item.order_number or 0), item.id)),
                start=1,
            )
        }
        base_pos = min(current_pos[qid] for qid in ordered_ids)
        for idx, qid in enumerate(ordered_ids):
            question_map[qid].order_index = base_pos + idx
            question_map[qid].order_number = base_pos + idx

        normalized = sorted(questions, key=lambda item: ((item.order_index or item.order_number or 0), item.id))
        for idx, question in enumerate(normalized, start=1):
            question.order_index = idx
            question.order_number = idx
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f'Error reordering questions: {e}')
        return jsonify({'success': False, 'error': 'Could not reorder questions'}), 500


@admin_quiz_bp.route('/quiz/<int:quiz_id>/import/paste', methods=['POST'])
@admin_required
def import_quiz_questions_from_paste(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    raw_text = request.form.get('bulk_text', '')
    parsed = _parse_question_blocks(raw_text)
    if not parsed:
        flash('No valid questions found in pasted text.', 'warning')
        return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))
    try:
        next_order = _next_question_order(quiz.id)
        for item in parsed:
            q = QuizQuestion(
                quiz_id=quiz.id,
                question_text=item['question_text'],
                question_type=item['question_type'],
                option_a=item.get('option_a'),
                option_b=item.get('option_b'),
                option_c=item.get('option_c'),
                option_d=item.get('option_d'),
                correct_answer=item['correct_answer'],
                order_index=next_order,
                order_number=next_order,
            )
            next_order += 1
            db.session.add(q)
        db.session.commit()
        flash(f'Imported {len(parsed)} questions from text.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error importing pasted questions: {e}')
        flash('Could not import questions.', 'danger')
    return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))


@admin_quiz_bp.route('/quiz/<int:quiz_id>/import/file', methods=['POST'])
@admin_required
def import_quiz_questions_from_file(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    upload = request.files.get('question_file')
    if not upload or not upload.filename:
        flash('Please select a file to import.', 'danger')
        return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))
    try:
        extracted_text = _extract_text_from_upload(upload)
        parsed = _parse_question_blocks(extracted_text)
        if not parsed:
            flash('No valid questions found in uploaded file.', 'warning')
            return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))

        next_order = _next_question_order(quiz.id)
        for item in parsed:
            question = QuizQuestion(
                quiz_id=quiz.id,
                question_text=item['question_text'],
                question_type=item['question_type'],
                option_a=item.get('option_a'),
                option_b=item.get('option_b'),
                option_c=item.get('option_c'),
                option_d=item.get('option_d'),
                correct_answer=item['correct_answer'],
                order_index=next_order,
                order_number=next_order,
            )
            next_order += 1
            db.session.add(question)
        db.session.commit()
        flash(f'Imported {len(parsed)} questions from file.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error importing from file: {e}')
        flash(str(e), 'danger')
    return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))


@admin_quiz_bp.route('/quiz/<int:quiz_id>/generate-from-lesson', methods=['POST'])
@admin_required
def generate_quiz_from_lesson(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    lesson_id = request.form.get('lesson_id', type=int)
    if not lesson_id:
        flash('Please select a lesson.', 'danger')
        return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))

    lesson = Video.query.filter_by(id=lesson_id, course_id=quiz.course_id).first()
    if not lesson:
        flash('Selected lesson does not belong to this course.', 'danger')
        return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))

    from services.ai_quiz_generator import generate_quiz_from_lesson as generate_service
    generated = generate_service(lesson.id)
    if not generated:
        flash('Generator returned no questions for this lesson.', 'warning')
        return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))

    try:
        next_order = _next_question_order(quiz.id)
        for item in generated:
            db.session.add(QuizQuestion(
                quiz_id=quiz.id,
                question_text=item.get('question_text', '').strip(),
                question_type='mcq',
                option_a=item.get('option_a', '').strip(),
                option_b=item.get('option_b', '').strip(),
                option_c=item.get('option_c', '').strip(),
                option_d=item.get('option_d', '').strip(),
                correct_answer=(item.get('correct_answer') or 'A').strip().upper()[:1],
                order_index=next_order,
                order_number=next_order,
            ))
            next_order += 1
        db.session.commit()
        flash(f'Generated {len(generated)} questions from lesson content.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Error generating quiz from lesson: {e}')
        flash('Could not generate quiz from lesson.', 'danger')
    return redirect(url_for('admin_quiz.manage_quiz_questions', quiz_id=quiz.id))

