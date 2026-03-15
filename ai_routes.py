from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename

from models import CodingChallenge, CodingSubmission, Enrollment, InterviewSession, ProjectIdea, StudentProject, Video, UserResume, db
from student_routes import student_required
from services.ai.career_service import CAREER_ROADMAPS, generate_career_roadmap
from services.ai.project_idea_service import PROJECT_IDEAS, generate_project_ideas, normalize_domain
from services.ai.recommendation_service import recommend_courses
from services.ai.learning.notes_service import generate_notes
from services.ai.learning.quiz_generator_service import generate_quiz_from_lesson
from services.ai.learning.revision_service import get_revision_topics
from services.ai.learning.study_planner_service import generate_study_plan
from services.ai.skills.skill_graph_service import build_skill_graph
from services.ai.career.resume_service import CAREER_SKILL_MAP, analyze_resume
from services.ai.career.resume_parser_service import extract_text_from_docx, extract_text_from_pdf, parse_resume
from services.ai.career.skill_gap_service import detect_skill_gap
from services.ai.career.portfolio_service import generate_portfolio
from services.ai.coding import (
    analyze_code_solution,
    create_submission,
    evaluate_submission,
    get_coding_challenges,
    update_skill_progress_for_challenge,
)
from services.ai.interview import (
    SUPPORTED_INTERVIEW_ROLES,
    get_recent_interview_sessions,
    get_session_detail,
    start_interview,
    submit_interview_answers,
)
from services.ai.projects import (
    generate_project,
    get_recent_student_projects,
    get_student_project_detail,
    start_student_project,
    update_student_project_progress,
)
from services.ai.devtools import (
    SUPPORTED_TOPICS,    analyze_project_structure,
    explain_error,
    generate_coding_problem,
)
import os
import json
import uuid
import zipfile


ai_bp = Blueprint("ai", __name__, url_prefix="/student/ai")
career_bp = Blueprint("career_ai", __name__, url_prefix="/student/career")
devtools_bp = Blueprint("devtools", __name__, url_prefix="/student/devtools")
skills_bp = Blueprint("skills", __name__, url_prefix="/student")
coding_bp = Blueprint("coding", __name__, url_prefix="/student/coding")
interview_bp = Blueprint("interview", __name__, url_prefix="/student/interview")
project_bp = Blueprint("projects", __name__, url_prefix="/student/projects")
RESUME_UPLOAD_DIR = os.path.join("uploads", "resumes")
DEVTOOLS_UPLOAD_DIR = os.path.join("uploads", "devtools")
ALLOWED_RESUME_EXTENSIONS = {".txt", ".pdf", ".docx"}
ALLOWED_CODEBASE_EXTENSIONS = {".zip", ".txt", ".py", ".js", ".json", ".md"}


def _student_enrollments(user_id):
    return Enrollment.query.filter_by(user_id=user_id).all()


def _preferred_domain_for_user(user_id):
    enrollments = _student_enrollments(user_id)
    for enrollment in enrollments:
        if enrollment.course and enrollment.course.domain:
            return enrollment.course.domain.name
    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    if resume_row:
        skills = json.loads(resume_row.skills_json or "[]")
        inferred = _domain_from_resume_skills(skills)
        if inferred:
            return inferred
    return "AI"


def _domain_from_resume_skills(skills: list[str]) -> str:
    if any(skill in skills for skill in ["React", "JavaScript", "HTML", "CSS"]):
        return "Web Development"
    if any(skill in skills for skill in ["Machine Learning", "Deep Learning", "Neural Networks"]):
        return "AI"
    if any(skill in skills for skill in ["Pandas", "Statistics", "Visualization"]):
        return "Data Science"
    if any(skill in skills for skill in ["Flutter", "Android", "Kotlin", "Swift"]):
        return "Mobile Apps"
    return "AI"


def _get_accessible_video(video_id):
    video = Video.query.get_or_404(video_id)
    enrollment = Enrollment.query.filter_by(user_id=session["user_id"], course_id=video.course_id).first()
    if not enrollment:
        flash("Please enroll in the course to access this AI learning tool.", "warning")
        return None, redirect(url_for("student.my_courses"))
    return video, None


def _extract_resume_text(file_storage):
    if not file_storage or not file_storage.filename:
        return ""
    _, extension = os.path.splitext(file_storage.filename)
    extension = extension.lower()
    if extension not in ALLOWED_RESUME_EXTENSIONS:
        return ""
    raw_bytes = file_storage.read()
    file_storage.stream.seek(0)
    if extension == ".txt":
        return raw_bytes.decode("utf-8", errors="ignore")

    os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)
    safe_name = secure_filename(file_storage.filename)
    temp_name = f"_tmp_{safe_name}" if safe_name else f"_tmp_resume{extension}"
    temp_path = os.path.join(RESUME_UPLOAD_DIR, temp_name)
    with open(temp_path, "wb") as temp_file:
        temp_file.write(raw_bytes)

    extracted = ""
    if extension == ".pdf":
        extracted = extract_text_from_pdf(temp_path)
    elif extension == ".docx":
        extracted = extract_text_from_docx(temp_path)

    try:
        os.remove(temp_path)
    except OSError:
        pass
    return extracted


def _save_resume_file(file_storage, user_id: int) -> tuple[str, str]:
    if not file_storage or not file_storage.filename:
        return "", ""
    filename = secure_filename(file_storage.filename)
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    if extension not in ALLOWED_RESUME_EXTENSIONS:
        return "", ""
    os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)
    safe_name = filename or f"resume_{user_id}{extension}"
    unique_name = f"{os.path.splitext(safe_name)[0]}_{user_id}_{uuid.uuid4().hex[:6]}{extension}"
    full_path = os.path.join(RESUME_UPLOAD_DIR, unique_name)
    file_storage.save(full_path)
    return os.path.join("resumes", unique_name), full_path


def _resume_row_to_analysis(resume_row: UserResume) -> dict:
    skills = json.loads(resume_row.skills_json or "[]")
    career_scores = []
    for career, required_skills in CAREER_SKILL_MAP.items():
        score = sum(1 for skill in required_skills if skill in skills)
        if score > 0:
            career_scores.append((career, score))
    career_scores.sort(key=lambda item: item[1], reverse=True)
    primary_career = career_scores[0][0] if career_scores else "Full Stack Developer"
    missing = [skill for skill in CAREER_SKILL_MAP[primary_career] if skill not in skills]
    suggestions = []
    if not skills:
        suggestions.append("Add a clear skills section listing the technologies you used.")
    if missing:
        suggestions.append(f"Strengthen these skills for {primary_career}: {', '.join(missing[:4])}.")
    return {
        "detected_skills": skills,
        "missing_skills": missing,
        "suggestions": suggestions,
        "career_matches": [item[0] for item in career_scores[:3]] or [primary_career],
        "experience_indicators": json.loads(resume_row.experience_json or "[]"),
    }


def _extract_codebase_files(file_storage, pasted_code):
    file_list = []

    if pasted_code:
        for line in pasted_code.splitlines():
            cleaned = line.strip()
            if cleaned:
                file_list.append(cleaned)

    if not file_storage or not file_storage.filename:
        return file_list

    filename = secure_filename(file_storage.filename)
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    if extension not in ALLOWED_CODEBASE_EXTENSIONS:
        return file_list

    raw_bytes = file_storage.read()
    file_storage.stream.seek(0)

    if extension == ".zip":
        archive_path = os.path.join(DEVTOOLS_UPLOAD_DIR, filename)
        with open(archive_path, "wb") as archive_file:
            archive_file.write(raw_bytes)
        with zipfile.ZipFile(archive_path, "r") as archive:
            file_list.extend(member for member in archive.namelist() if member and not member.endswith("/"))
        return file_list

    decoded = raw_bytes.decode("utf-8", errors="ignore")
    file_list.extend(line.strip() for line in decoded.splitlines() if line.strip())
    return file_list



@ai_bp.route("/project-ideas")
@student_required
def project_ideas():
    selected_domain = request.args.get("domain", "").strip() or _preferred_domain_for_user(session["user_id"])
    normalized_domain = normalize_domain(selected_domain)
    domains = list(PROJECT_IDEAS.keys())
    ideas = generate_project_ideas(normalized_domain)
    return render_template(
        "student/ai/project_ideas.html",
        selected_domain=normalized_domain,
        domains=domains,
        ideas=ideas,
    )


@ai_bp.route("/career-roadmap")
@student_required
def career_roadmap():
    roles = list(CAREER_ROADMAPS.keys())
    selected_role = request.args.get("role", "").strip() or "Full Stack Developer"
    roadmap = generate_career_roadmap(selected_role, user_id=session["user_id"])
    return render_template(
        "student/career/roadmap.html",
        roles=roles,
        selected_role=roadmap["role"],
        roadmap=roadmap,
    )


@ai_bp.route("/recommendations")
@student_required
def recommendations():
    recommended_courses = recommend_courses(session["user_id"])
    return render_template(
        "student/ai/recommendations.html",
        recommended_courses=recommended_courses,
    )


@ai_bp.route("/study-planner")
@student_required
def study_planner():
    enrollments = [row for row in _student_enrollments(session["user_id"]) if row.course]
    selected_course_id = request.args.get("course_id", type=int)
    days = max(1, min(30, request.args.get("days", type=int) or 7))

    if not selected_course_id and enrollments:
        selected_course_id = enrollments[0].course_id

    plan = None
    enrolled_ids = {row.course_id for row in enrollments}
    if selected_course_id and selected_course_id in enrolled_ids:
        plan = generate_study_plan(session["user_id"], selected_course_id, days)

    return render_template(
        "student/ai/study_planner.html",
        enrollments=enrollments,
        selected_course_id=selected_course_id,
        selected_days=days,
        plan=plan,
    )


@ai_bp.route("/notes/<int:video_id>")
@student_required
def notes(video_id):
    video, blocked = _get_accessible_video(video_id)
    if blocked:
        return blocked
    notes_payload = generate_notes(video_id)
    return render_template(
        "student/ai/notes.html",
        video=video,
        notes=notes_payload,
    )


@ai_bp.route("/practice-quiz/<int:video_id>", methods=["GET", "POST"])
@student_required
def practice_quiz(video_id):
    video, blocked = _get_accessible_video(video_id)
    if blocked:
        return blocked

    questions = generate_quiz_from_lesson(video_id)
    results = []
    score = None
    if request.method == "POST":
        correct_count = 0
        for index, question in enumerate(questions):
            submitted = (request.form.get(f"question_{index}") or "").strip()
            is_correct = submitted == question["correct_answer"]
            if is_correct:
                correct_count += 1
            results.append(
                {
                    "question": question["question"],
                    "selected_answer": submitted,
                    "correct_answer": question["correct_answer"],
                    "is_correct": is_correct,
                }
            )
        score = {
            "correct": correct_count,
            "total": len(questions),
            "percentage": round((correct_count / len(questions)) * 100, 2) if questions else 0,
        }

    return render_template(
        "student/ai/practice_quiz.html",
        video=video,
        questions=questions,
        results=results,
        score=score,
    )


@ai_bp.route("/revision")
@student_required
def revision():
    revision_topics = get_revision_topics(session["user_id"])
    return render_template(
        "student/ai/revision.html",
        revision_topics=revision_topics,
    )


@career_bp.route("/resume-analyzer", methods=["GET", "POST"])
@student_required
def resume_analyzer():
    analysis = None
    resume_text = ""
    resume_row = UserResume.query.filter_by(user_id=session["user_id"]).first()
    os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)
    if request.method == "POST":
        resume_text = (request.form.get("resume_text") or "").strip()
        uploaded_file = request.files.get("resume_file")
        if uploaded_file and uploaded_file.filename:
            resume_path, _ = _save_resume_file(uploaded_file, session["user_id"])
            extracted = _extract_resume_text(uploaded_file)
            if extracted:
                resume_text = extracted
            if resume_path:
                if resume_row and resume_row.resume_path and resume_row.resume_path.startswith("resumes/"):
                    old_path = os.path.join("uploads", resume_row.resume_path)
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except OSError:
                            pass
                if resume_row:
                    resume_row.resume_path = resume_path

        if resume_text:
            parsed = parse_resume(resume_text)
            analysis = analyze_resume(resume_text)
            if not resume_row:
                resume_row = UserResume(user_id=session["user_id"])
                db.session.add(resume_row)
            resume_row.skills_json = json.dumps(parsed.get("skills", []))
            resume_row.projects_json = json.dumps(parsed.get("projects", []))
            resume_row.education_json = json.dumps(parsed.get("education", []))
            resume_row.experience_json = json.dumps(parsed.get("experience", []))
            db.session.commit()
        elif resume_row and uploaded_file and uploaded_file.filename:
            resume_row.skills_json = json.dumps([])
            resume_row.projects_json = json.dumps([])
            resume_row.education_json = json.dumps([])
            resume_row.experience_json = json.dumps([])
            db.session.commit()
            analysis = _resume_row_to_analysis(resume_row)
        elif resume_row:
            analysis = _resume_row_to_analysis(resume_row)
        else:
            flash("Please paste resume text or upload a simple TXT, PDF, or DOCX file.", "warning")
    elif resume_row:
        analysis = _resume_row_to_analysis(resume_row)
    return render_template(
        "student/career/resume_analyzer.html",
        analysis=analysis,
        resume_text=resume_text,
        resume_exists=resume_row is not None,
    )


@career_bp.route("/skill-gap")
@student_required
def skill_gap():
    career_options = list(CAREER_SKILL_MAP.keys())
    selected_goal = request.args.get("career_goal", "").strip() or "Full Stack Developer"
    gap_report = detect_skill_gap(session["user_id"], selected_goal)
    return render_template(
        "student/career/skill_gap.html",
        career_options=career_options,
        selected_goal=selected_goal,
        gap_report=gap_report,
    )


@career_bp.route("/portfolio")
@student_required
def portfolio():
    portfolio_payload = generate_portfolio(session["user_id"])
    return render_template(
        "student/career/portfolio.html",
        portfolio=portfolio_payload,
    )


@devtools_bp.route("/coding-practice", methods=["GET", "POST"])
@student_required
def coding_practice():
    selected_topic = (request.values.get("topic") or "Python").strip()
    problem = generate_coding_problem(selected_topic)
    submitted_attempt = ""
    show_solution = False
    action = "run"
    result_summary = None

    if request.method == "POST":
        selected_topic = (request.form.get("topic") or selected_topic).strip()
        problem = generate_coding_problem(selected_topic)
        submitted_attempt = (request.form.get("attempt") or "").strip()
        show_solution = request.form.get("show_solution") == "1"
        action = (request.form.get("action") or "run").strip().lower()
        if submitted_attempt:
            status = "Ready to refine" if action == "run" else "Submission saved"
            feedback = problem["hints"][0]
            if action == "submit":
                feedback = "Good structure. Review the hints, verify edge cases, and compare your approach with the reference solution if needed."
            result_summary = {
                "test_cases_passed": "Preview mode",
                "status": status,
                "feedback": feedback,
            }
        else:
            flash("Add some code or a solution approach before running the practice tool.", "warning")

    return render_template(
        "student/devtools/coding_practice.html",
        topics=SUPPORTED_TOPICS,
        selected_topic=problem["topic"],
        problem=problem,
        submitted_attempt=submitted_attempt,
        show_solution=show_solution,
        action=action,
        result_summary=result_summary,
    )


@devtools_bp.route("/debug", methods=["GET", "POST"])
@student_required
def debug_assistant():
    error_text = ""
    analysis = None
    if request.method == "POST":
        error_text = (request.form.get("error_text") or "").strip()
        if error_text:
            analysis = explain_error(error_text)
        else:
            flash("Paste an error message or traceback to get debugging help.", "warning")
    return render_template(
        "student/devtools/debug_assistant.html",
        error_text=error_text,
        analysis=analysis,
    )


@devtools_bp.route("/codebase-explainer", methods=["GET", "POST"])
@student_required
def codebase_explainer():
    os.makedirs(DEVTOOLS_UPLOAD_DIR, exist_ok=True)
    pasted_files = ""
    analysis = None
    file_count = 0

    if request.method == "POST":
        pasted_files = (request.form.get("files_text") or "").strip()
        uploaded_file = request.files.get("project_file")
        files = _extract_codebase_files(uploaded_file, pasted_files)
        file_count = len(files)
        if files:
            analysis = analyze_project_structure(files)
        else:
            flash("Upload a ZIP/text file or paste file names to analyze a project structure.", "warning")

    return render_template(
        "student/devtools/codebase_explainer.html",
        pasted_files=pasted_files,
        analysis=analysis,
        file_count=file_count,
    )




@skills_bp.route("/skills")
@student_required
def skill_graph():
    skill_graph_payload = build_skill_graph(session["user_id"])
    return render_template(
        "student/skills/skill_graph.html",
        skill_graph=skill_graph_payload,
    )


@coding_bp.route("/challenges")
@student_required
def coding_challenges():
    topic_filter = (request.args.get("topic") or "").strip()
    challenges = get_coding_challenges(topic_filter or None)
    topics = sorted({challenge.topic for challenge in CodingChallenge.query.all()})
    return render_template(
        "student/coding/challenges.html",
        challenges=challenges,
        selected_topic=topic_filter,
        topics=topics,
    )


@coding_bp.route("/challenge/<int:id>")
@student_required
def coding_challenge_detail(id):
    challenge = CodingChallenge.query.get_or_404(id)
    latest_submission = CodingSubmission.query.filter_by(
        user_id=session["user_id"],
        challenge_id=challenge.id,
    ).order_by(CodingSubmission.submitted_at.desc()).first()
    return render_template(
        "student/coding/challenge_detail.html",
        challenge=challenge,
        test_cases=challenge.get_test_cases(),
        latest_submission=latest_submission,
    )


@coding_bp.route("/submit/<int:id>", methods=["POST"])
@student_required
def coding_submit(id):
    challenge = CodingChallenge.query.get_or_404(id)
    code = (request.form.get("code_submitted") or "").strip()
    if not code:
        flash("Please enter your code before running the challenge.", "warning")
        return redirect(url_for("coding.coding_challenge_detail", id=id))

    evaluation = evaluate_submission(code, challenge)
    submission = create_submission(session["user_id"], challenge, code, evaluation)
    if evaluation.get("score", 0) > 0:
        update_skill_progress_for_challenge(session["user_id"], challenge, evaluation["score"])
    return redirect(url_for("coding.coding_results", submission_id=submission.id))


@coding_bp.route("/results/<int:submission_id>")
@student_required
def coding_results(submission_id):
    submission = CodingSubmission.query.get_or_404(submission_id)
    if submission.user_id != session["user_id"]:
        flash("You can only view your own coding submissions.", "warning")
        return redirect(url_for("coding.coding_challenges"))

    challenge = submission.challenge
    evaluation = evaluate_submission(submission.code_submitted, challenge) if challenge else {
        "passed_tests": submission.passed_tests,
        "total_tests": 0,
        "score": submission.score,
        "results": [],
        "execution_output": submission.execution_output,
        "error": None,
    }
    feedback = analyze_code_solution(submission.code_submitted)
    return render_template(
        "student/coding/results.html",
        challenge=challenge,
        submission=submission,
        evaluation=evaluation,
        feedback=feedback,
    )


@interview_bp.route("")
@student_required
def interview_home():
    recent_sessions = get_recent_interview_sessions(session["user_id"])
    return render_template(
        "student/interview/interview_home.html",
        recent_sessions=recent_sessions,
        roles=SUPPORTED_INTERVIEW_ROLES,
    )


@interview_bp.route("/start", methods=["GET", "POST"])
@student_required
def interview_start():
    if request.method == "POST":
        role = (request.form.get("role") or "Full Stack Developer").strip()
        difficulty = (request.form.get("difficulty") or "Beginner").strip()
        interview_session = start_interview(session["user_id"], role, difficulty)
        return redirect(url_for("interview.interview_session_view", id=interview_session.id))

    return render_template(
        "student/interview/start_interview.html",
        roles=SUPPORTED_INTERVIEW_ROLES,
        difficulty_levels=["Beginner", "Intermediate", "Advanced"],
    )


@interview_bp.route("/session/<int:id>")
@student_required
def interview_session_view(id):
    detail = get_session_detail(id)
    interview_session = detail["session"]
    if interview_session.user_id != session["user_id"]:
        flash("You can only access your own interview session.", "warning")
        return redirect(url_for("interview.interview_home"))
    return render_template(
        "student/interview/interview_session.html",
        interview_session=interview_session,
        questions=detail["questions"],
        responses=detail["responses"],
        timer_minutes=20 if interview_session.difficulty != "Advanced" else 30,
    )


@interview_bp.route("/submit", methods=["POST"])
@student_required
def interview_submit():
    session_id = request.form.get("session_id", type=int)
    interview_session = InterviewSession.query.get_or_404(session_id)
    if interview_session.user_id != session["user_id"]:
        flash("You can only submit your own interview session.", "warning")
        return redirect(url_for("interview.interview_home"))

    answers = {}
    for question in interview_session.questions:
        answers[question.id] = request.form.get(f"question_{question.id}", "")

    submit_interview_answers(session_id, answers)
    return redirect(url_for("interview.interview_result", id=session_id))


@interview_bp.route("/result/<int:id>")
@student_required
def interview_result(id):
    detail = get_session_detail(id)
    interview_session = detail["session"]
    if interview_session.user_id != session["user_id"]:
        flash("You can only view your own interview result.", "warning")
        return redirect(url_for("interview.interview_home"))
    return render_template(
        "student/interview/interview_result.html",
        interview_session=interview_session,
        questions=detail["questions"],
        responses=detail["responses"],
    )


@project_bp.route("")
@student_required
def projects_home():
    recent_projects = get_recent_student_projects(session["user_id"])
    generated_projects = ProjectIdea.query.order_by(ProjectIdea.created_at.desc(), ProjectIdea.id.desc()).limit(6).all()
    return render_template(
        "student/projects/projects_home.html",
        recent_projects=recent_projects,
        generated_projects=generated_projects,
        domains=["AI", "Web Development", "Machine Learning", "Data Science", "Mobile Apps"],
        difficulty_levels=["Beginner", "Intermediate", "Advanced"],
    )


@project_bp.route("/generate", methods=["GET", "POST"])
@student_required
def project_generate():
    created_project = None
    if request.method == "POST":
        domain = (request.form.get("domain") or "").strip()
        if not domain:
            resume_row = UserResume.query.filter_by(user_id=session["user_id"]).first()
            if resume_row:
                resume_skills = json.loads(resume_row.skills_json or "[]")
                domain = _domain_from_resume_skills(resume_skills)
        domain = domain or "AI"
        difficulty = (request.form.get("difficulty") or "Beginner").strip()
        created_project = generate_project(domain, difficulty)

    return render_template(
        "student/projects/project_generator.html",
        created_project=created_project,
        domains=["AI", "Web Development", "Machine Learning", "Data Science", "Mobile Apps"],
        difficulty_levels=["Beginner", "Intermediate", "Advanced"],
    )


@project_bp.route("/<int:id>")
@student_required
def project_detail(id):
    project = ProjectIdea.query.get_or_404(id)
    student_project = StudentProject.query.filter_by(user_id=session["user_id"], project_id=project.id).first()
    project_detail_payload = get_student_project_detail(student_project.id) if student_project else None
    return render_template(
        "student/projects/project_detail.html",
        project=project,
        student_project=student_project,
        project_detail=project_detail_payload,
    )


@project_bp.route("/start/<int:id>", methods=["POST"])
@student_required
def project_start(id):
    student_project = start_student_project(session["user_id"], id)
    return redirect(url_for("projects.project_progress", id=student_project.id))


@project_bp.route("/progress/<int:id>", methods=["GET", "POST"])
@student_required
def project_progress(id):
    student_project = StudentProject.query.get_or_404(id)
    if student_project.user_id != session["user_id"]:
        flash("You can only manage your own projects.", "warning")
        return redirect(url_for("projects.projects_home"))

    if request.method == "POST":
        completed_task_ids = request.form.getlist("completed_tasks")
        student_project = update_student_project_progress(id, completed_task_ids)

    detail = get_student_project_detail(student_project.id)
    return render_template(
        "student/projects/project_progress.html",
        student_project=detail["student_project"],
        project=detail["project"],
        tasks=detail["tasks"],
        blueprint=detail["blueprint"],
    )



