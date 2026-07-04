from flask import Flask, render_template, session, request, jsonify, send_from_directory, abort, current_app, redirect, url_for
from backend.models import db, User, AdminUser
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import text
import os
import sqlite3
import re
import glob
import unicodedata
import secrets

# Initialize environment
load_dotenv(override=True)

# Initialize Flask app

base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)
app = Flask(__name__, template_folder=os.path.join(root_dir, 'frontend', 'templates'), static_folder=os.path.join(root_dir, 'frontend', 'static'))

# Debug environment flags (safe values only)
print('MENTRA_USE_MYSQL =', os.getenv('MENTRA_USE_MYSQL'))
print('MENTRA_MYSQL_HOST =', os.getenv('MENTRA_MYSQL_HOST'))
print('MENTRA_MYSQL_DB =', os.getenv('MENTRA_MYSQL_DB'))
print("MENTRA_USE_MONGO =", os.getenv("MENTRA_USE_MONGO"))
print("MENTRA_MONGO_DB =", os.getenv("MENTRA_MONGO_DB"))


# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mentra-dev-secret-key')
default_sqlite_uri = f"sqlite:///{os.path.join(base_dir, 'instance', 'portal.db')}"
use_mysql = os.getenv('MENTRA_USE_MYSQL', 'false').lower() == 'true'

app.config['SQLALCHEMY_DATABASE_URI'] = default_sqlite_uri
if use_mysql:
    db_user = os.getenv('MENTRA_MYSQL_USER')
    db_pass = os.getenv('MENTRA_MYSQL_PASSWORD')
    db_host = os.getenv('MENTRA_MYSQL_HOST', 'localhost')
    db_port = os.getenv('MENTRA_MYSQL_PORT', '3306')
    db_name = os.getenv('MENTRA_MYSQL_DB')

    if all([db_user, db_pass, db_name]):
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
    else:
        use_mysql = False
        print('MySQL env vars missing; falling back to SQLite.')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Debug active DB URI (mask password if present)
active_uri = app.config['SQLALCHEMY_DATABASE_URI']
if active_uri and '@' in active_uri and '://' in active_uri:
    prefix, rest = active_uri.split('://', 1)
    if '@' in rest and ':' in rest.split('@')[0]:
        creds, hostpart = rest.split('@', 1)
        user = creds.split(':', 1)[0]
        active_uri = f"{prefix}://{user}:***@{hostpart}"
print('Active Database URI:', active_uri)


# Initialize MongoDB
mongo_client = None
mongo_db = None

if os.getenv("MENTRA_USE_MONGO", "false").lower() == "true":
    try:
        mongo_uri = os.getenv("MENTRA_MONGO_URI")
        mongo_db_name = os.getenv("MENTRA_MONGO_DB")

        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        mongo_client.server_info()  # forces connection

        mongo_db = mongo_client[mongo_db_name]

        print(f"[PID {os.getpid()}] MongoDB connected successfully: {mongo_db_name}")

    except Exception as e:
        print(f"[PID {os.getpid()}] MongoDB connection failed: {e}")
        mongo_db = None

# Register mongo_db in app context
app.mongo_db = mongo_db
app.config['MONGO_DB'] = mongo_db
print(f"[PID {os.getpid()}] App object ID: {id(app)}, mongo_db present: {mongo_db is not None}")

from flask_migrate import Migrate

# Initialize Database
db.init_app(app)
migrate = Migrate(app, db)

# Import and register blueprints
from backend.auth_routes import auth_bp
from backend.student_routes import student_bp
from backend.referral_routes import referral_bp
from backend.admin_routes import admin_bp
from backend.public_routes import public_bp
from backend.admin_quiz_routes import admin_quiz_bp
from backend.admin_assignment_routes import admin_assignment_bp
from backend.student_quiz_routes import student_quiz_bp
from backend.student_assignment_routes import student_assignment_bp
from backend.ai_routes import ai_bp, career_bp, coding_bp, devtools_bp, interview_bp, project_bp, skills_bp
from backend.community_routes import community_bp
from backend.routes.coding_api_routes import coding_api_bp
from backend.routes.orchestrator_api_routes import orchestrator_api_bp
from backend.routes.interview_routes import interview_api_bp
from backend.routes.ai_enhancements import ai_enhancements_bp
from backend.routes.learning_routes import learning_routes_bp
from backend.routes.experience_routes import experience_routes_bp
from backend.routes.twin_routes import twin_bp
from backend.routes.assessment_routes import assessment_bp
from backend.routes.memory_routes import memory_bp
from backend.routes.privacy_routes import privacy_bp
from backend.routes.explainability_routes import explainability_bp
from backend.routes.dashboard_routes import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(referral_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(public_bp)
app.register_blueprint(admin_quiz_bp)
app.register_blueprint(admin_assignment_bp)
app.register_blueprint(student_quiz_bp)
app.register_blueprint(student_assignment_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(career_bp)
app.register_blueprint(devtools_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(coding_bp)
app.register_blueprint(interview_bp)
app.register_blueprint(project_bp)
app.register_blueprint(community_bp)
app.register_blueprint(coding_api_bp)
app.register_blueprint(orchestrator_api_bp)
app.register_blueprint(interview_api_bp)
app.register_blueprint(ai_enhancements_bp)
app.register_blueprint(learning_routes_bp)
app.register_blueprint(experience_routes_bp)
app.register_blueprint(twin_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(memory_bp)
app.register_blueprint(privacy_bp)
app.register_blueprint(explainability_bp)
app.register_blueprint(dashboard_bp)

# Register Phase 5 Enterprise Observability Middleware
from backend.services.observability.middleware import observability_middleware
observability_middleware(app)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    safe_root = os.path.join(app.root_path, 'uploads')
    full_path = os.path.abspath(os.path.join(safe_root, filename))
    if os.path.commonpath([os.path.abspath(safe_root), full_path]) != os.path.abspath(safe_root):
        abort(404)
    if not os.path.exists(full_path):
        abort(404)
    rel_dir = os.path.dirname(filename)
    rel_name = os.path.basename(filename)
    return send_from_directory(os.path.join(safe_root, rel_dir), rel_name, as_attachment=False)


@app.route('/dashboard/job-score')
def job_score_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard/job_score.html')

@app.route('/dashboard/overview')
def dashboard_overview_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('student_overview_page'))


@app.route('/student/overview')
def student_overview_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard/overview.html')

@app.route('/student/learning-path')
def learning_path_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('learning/path.html')

@app.route('/student/weekly-report')
def weekly_report_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('learning/weekly_report.html')

@app.route('/student/flashcards')
def flashcards_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('learning/flashcards.html')

@app.route('/student/doubt-solver')
def doubt_solver_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('learning/doubt_solver.html')

@app.route('/student/resume-improver')
def resume_improver_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('career/resume_improver.html')

@app.route('/db-check')
def db_check():
    role = session.get('role') or session.get('user_role')
    if role != 'admin':
        return jsonify({"error": "Forbidden"}), 403
    try:
        if use_mysql:
            result = db.session.execute(text('SELECT DATABASE()'))
            row = result.fetchone()
            return jsonify({'success': True, 'data': {'database': (row[0] if row else None), 'driver': 'mysql'}})
        return jsonify({'success': True, 'data': {'database': 'sqlite', 'driver': 'sqlite'}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/mongo-check")
def mongo_check():
    role = session.get('role') or session.get('user_role')
    if role != 'admin':
        return jsonify({"error": "Forbidden"}), 403
    pid = os.getpid()
    use_mongo = os.getenv("MENTRA_USE_MONGO", "false").lower() == "true"
    
    # Try to get existing or connect on-demand for verification
    m_db = getattr(current_app, 'mongo_db', None)
    if m_db is None:
        m_db = current_app.config.get('MONGO_DB')
    
    print(f"[PID {pid}] mongo_check hit. App ID: {id(current_app._get_current_object())}, m_db present: {m_db is not None}")

    if m_db is None and use_mongo:
        try:
            from pymongo import MongoClient
            uri = os.getenv("MENTRA_MONGO_URI")
            db_name = os.getenv("MENTRA_MONGO_DB")
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.server_info()
            m_db = client[db_name]
            # Update app context
            current_app.mongo_db = m_db
            current_app.config['MONGO_DB'] = m_db
        except Exception as e:
            return jsonify({"error": f"On-demand connection failed: {e}", "pid": pid}), 500

    if m_db is None:
        return jsonify({
            "success": True,
            "data": {
                "status": "failed",
                "message": "MongoDB not connected (MENTRA_USE_MONGO is false or connection failed)",
                "debug": {"pid": pid, "use_mongo": use_mongo}
            }
        }), 200

    try:
        collections = m_db.list_collection_names()
        return jsonify({
            "success": True,
            "data": {
                "status": "connected",
                "database": m_db.name,
                "collections": collections,
                "debug": {"pid": pid}
            }
        })
    except Exception as e:
        return jsonify({"error": str(e), "debug": {"pid": pid}}), 500

from datetime import datetime, timezone

@app.route("/mongo-test-insert")
def mongo_test_insert():
    role = session.get('role') or session.get('user_role')
    if role != 'admin':
        return jsonify({"error": "Forbidden"}), 403
    m_db = getattr(current_app, 'mongo_db', None)
    if m_db is None:
        m_db = current_app.config.get('MONGO_DB')
    if m_db is None:
        # Try one-time connect for test
        try:
            from pymongo import MongoClient
            client = MongoClient(os.getenv("MENTRA_MONGO_URI"), serverSelectionTimeoutMS=5000)
            m_db = client[os.getenv("MENTRA_MONGO_DB")]
        except:
            return jsonify({"error": "Mongo not connected"}), 500

    try:
        m_db["test_collection"].insert_one({
            "test": "connection_check",
            "created_at": datetime.utcnow()
        })
        return jsonify({"success": True, "data": {"message": "Insert successful"}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _table_exists(conn, table_name):
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    ).fetchone()
    return row is not None


def _get_columns(conn, table_name):
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1] for row in rows}


def _build_referral_code(name, user_id, existing_codes):
    base_name = (name or "USER").upper().replace(" ", "")
    code_base = (base_name[:6] + str(user_id))[:12]
    candidate = code_base
    suffix = 1

    while not candidate or candidate in existing_codes:
        trimmed = code_base[:10]
        candidate = f"{trimmed}{suffix:02d}"[:12]
        suffix += 1

    existing_codes.add(candidate)
    return candidate


def _normalize_underscore(text):
    text = unicodedata.normalize('NFKD', (text or '')).encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


def _sync_course_image_references():
    """
    Align course.image_url with files in static/images/courses using a stable underscore naming convention.
    """
    images_dir = os.path.join(app.root_path, 'static', 'images', 'courses')
    if not os.path.isdir(images_dir):
        return

    file_map = {}
    for path in glob.glob(os.path.join(images_dir, '*.*')):
        file_name = os.path.basename(path)
        base = os.path.splitext(file_name)[0].lower()
        file_map[base] = file_name

    course_image_map = {
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
        "python data science": "python_datascience.jpg",
        "react js": "react_js.png",
        "react native": "react_native.png",
    }

    changed = False
    from models import Course
    courses = Course.query.all()
    for course in courses:
        title = (course.title or '').strip()
        candidates = []
        normalized = _normalize_underscore(title)
        if normalized:
            candidates.extend([normalized, normalized.replace('_', '')])

        title_lower = title.lower()
        for key, file_name in course_image_map.items():
            if key in title_lower:
                mapped_base = os.path.splitext(file_name)[0]
                candidates.extend([mapped_base, mapped_base.replace('_', '')])

        current = (course.image_url or '').strip()
        if current and current.startswith(('http://', 'https://', '/static/', 'static/')):
            continue

        # Keep already-valid local filename, but normalize basename case if needed.
        if current:
            current_base = os.path.splitext(os.path.basename(current))[0].lower()
            if current_base in file_map:
                expected = file_map[current_base]
                if current != expected:
                    course.image_url = expected
                    changed = True
                continue

        for candidate in candidates:
            matched = file_map.get(candidate.lower())
            if matched:
                if course.image_url != matched:
                    course.image_url = matched
                    changed = True
                break

    if changed:
        db.session.commit()


def _repair_legacy_schema(database_path):
    """
    Best-effort SQLite schema repair for older local DB files.
    This keeps existing data and adds missing columns expected by current models.
    """
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    with sqlite3.connect(database_path) as conn:
        expected_columns = {
            "users": [
                "name TEXT",
                "email TEXT",
                "password TEXT",
                "role TEXT DEFAULT 'student'",
                "referral_code TEXT",
                "referred_by TEXT",
                "wallet_balance REAL DEFAULT 0.0",
                "created_at DATETIME",
            ],
            "domains": [
                "name TEXT",
                "description TEXT",
                "image_url TEXT",
                "created_at DATETIME",
            ],
            "courses": [
                "title TEXT",
                "description TEXT",
                "domain_id INTEGER",
                "price REAL DEFAULT 0.0",
                "instructor TEXT",
                "image_url TEXT",
                "demo_video_url TEXT",
                "status TEXT DEFAULT 'draft'",
                "created_at DATETIME",
            ],
            "syllabuses": [
                "course_id INTEGER",
                "topic_title TEXT",
                "topic_description TEXT",
                "order_number INTEGER DEFAULT 0",
                "created_at DATETIME",
            ],
            "videos": [
                "course_id INTEGER",
                "title TEXT",
                "video_url TEXT",
                "description TEXT",
                "duration TEXT",
                "module_id INTEGER",
                "order_number INTEGER DEFAULT 0",
                "created_at DATETIME",
            ],
            "enrollments": [
                "user_id INTEGER",
                "course_id INTEGER",
                "enrolled_date DATETIME",
                "progress REAL DEFAULT 0.0",
                "progress_percentage REAL DEFAULT 0.0",
                "completed BOOLEAN DEFAULT 0",
            ],
            "contact_messages": [
                "name TEXT",
                "email TEXT",
                "subject TEXT",
                "message TEXT",
                "created_at DATETIME",
            ],
            "referral_transactions": [
                "referrer_id INTEGER",
                "new_user_id INTEGER",
                "reward_amount REAL DEFAULT 100.0",
                "status TEXT DEFAULT 'completed'",
                "date DATETIME",
            ],
            "chatbot_conversations": [
                "user_id INTEGER",
                "course_id INTEGER",
                "user_message TEXT",
                "bot_response TEXT",
                "domain TEXT",
                "timestamp DATETIME",
            ],
            "admin_users": [
                "user_id INTEGER",
                "username TEXT",
                "password TEXT",
                "full_name TEXT",
                "email TEXT",
                "role TEXT DEFAULT 'super_admin'",
                "is_active BOOLEAN DEFAULT 1",
                "created_at DATETIME",
                "last_login DATETIME",
                "password_changed_at DATETIME",
            ],
            "audit_logs": [
                "entity_type TEXT",
                "entity_id INTEGER",
                "action_type TEXT",
                "actor_id INTEGER",
                "actor_role TEXT",
                "before_values TEXT",
                "after_values TEXT",
                "metadata_json TEXT",
                "created_at DATETIME",
            ],
            "quizzes": [
                "course_id INTEGER",
                "title TEXT",
                "description TEXT",
                "question_count_target INTEGER DEFAULT 10",
                "passing_percentage REAL DEFAULT 60.0",
                "time_limit_minutes INTEGER DEFAULT 15",
                "attempts_allowed INTEGER DEFAULT 3",
                "is_enabled BOOLEAN DEFAULT 1",
                "module_id INTEGER",
                "created_at DATETIME",
            ],
            "quiz_questions": [
                "quiz_id INTEGER",
                "question_text TEXT",
                "question_type TEXT DEFAULT 'mcq'",
                "option_a TEXT",
                "option_b TEXT",
                "option_c TEXT",
                "option_d TEXT",
                "correct_answer TEXT",
                "order_index INTEGER DEFAULT 1",
                "order_number INTEGER DEFAULT 1",
                "created_at DATETIME",
            ],
            "quiz_attempts": [
                "quiz_id INTEGER",
                "user_id INTEGER",
                "attempt_number INTEGER DEFAULT 1",
                "total_questions INTEGER DEFAULT 0",
                "correct_answers INTEGER DEFAULT 0",
                "score_percentage REAL DEFAULT 0.0",
                "passed BOOLEAN DEFAULT 0",
                "start_time DATETIME",
                "end_time DATETIME",
                "started_at DATETIME",
                "submitted_at DATETIME",
            ],
            "quiz_answers": [
                "attempt_id INTEGER",
                "question_id INTEGER",
                "submitted_answer TEXT",
                "is_correct BOOLEAN DEFAULT 0",
                "created_at DATETIME",
            ],
            "assignments": [
                "course_id INTEGER",
                "title TEXT",
                "instructions TEXT",
                "due_date DATETIME",
                "marks REAL DEFAULT 100.0",
                "module_id INTEGER",
                "attachment_path TEXT",
                "created_at DATETIME",
            ],
            "course_modules": [
                "course_id INTEGER",
                "title TEXT",
                "order_index INTEGER DEFAULT 1",
                "created_at DATETIME",
            ],
            "assignment_submissions": [
                "assignment_id INTEGER",
                "user_id INTEGER",
                "answer_text TEXT",
                "submission_file TEXT",
                "submitted_at DATETIME",
                "marks_awarded REAL",
                "feedback TEXT",
                "graded_at DATETIME",
            ],
            "lesson_progress": [
                "user_id INTEGER",
                "lesson_id INTEGER",
                "course_id INTEGER",
                "completed BOOLEAN DEFAULT 0",
                "completed_at DATETIME",
                "created_at DATETIME",
            ],
            "learning_streaks": [
                "user_id INTEGER",
                "last_learning_date DATE",
                "current_streak INTEGER DEFAULT 0",
                "longest_streak INTEGER DEFAULT 0",
                "updated_at DATETIME",
            ],
            "skill_progress": [
                "user_id INTEGER",
                "skill_name TEXT",
                "progress_percentage REAL DEFAULT 0.0",
                "last_updated DATETIME",
            ],
            "coding_challenges": [
                "title TEXT",
                "description TEXT",
                "difficulty TEXT DEFAULT 'Beginner'",
                "topic TEXT",
                "starter_code TEXT",
                "expected_output TEXT",
                "test_cases_json TEXT DEFAULT '[]'",
                "created_at DATETIME",
            ],
            "coding_submissions": [
                "user_id INTEGER",
                "challenge_id INTEGER",
                "code_submitted TEXT",
                "execution_output TEXT",
                "passed_tests INTEGER DEFAULT 0",
                "score REAL DEFAULT 0.0",
                "submitted_at DATETIME",
            ],
            "interview_sessions": [
                "user_id INTEGER",
                "role TEXT",
                "difficulty TEXT DEFAULT 'Beginner'",
                "start_time DATETIME",
                "end_time DATETIME",
                "score REAL DEFAULT 0.0",
                "status TEXT DEFAULT 'in_progress'",
            ],
            "interview_questions": [
                "session_id INTEGER",
                "question_text TEXT",
                "question_type TEXT DEFAULT 'technical'",
                "expected_answer TEXT",
                "difficulty TEXT DEFAULT 'Beginner'",
            ],
            "interview_responses": [
                "session_id INTEGER",
                "question_id INTEGER",
                "user_answer TEXT",
                "ai_feedback TEXT",
                "score REAL DEFAULT 0.0",
            ],
            "project_ideas": [
                "title TEXT",
                "description TEXT",
                "domain TEXT",
                "difficulty TEXT DEFAULT 'Beginner'",
                "tech_stack TEXT",
                "architecture TEXT",
                "created_at DATETIME",
            ],
            "student_projects": [
                "user_id INTEGER",
                "project_id INTEGER",
                "progress_percentage REAL DEFAULT 0.0",
                "started_at DATETIME",
                "completed_at DATETIME",
            ],
            "project_tasks": [
                "project_id INTEGER",
                "task_title TEXT",
                "task_description TEXT",
                "task_order INTEGER DEFAULT 1",
                "completed BOOLEAN DEFAULT 0",
            ],
            "community_posts": [
                "user_id INTEGER",
                "title TEXT",
                "content TEXT",
                "created_at DATETIME",
            ],
            "community_answers": [
                "post_id INTEGER",
                "user_id INTEGER",
                "answer_text TEXT",
                "votes INTEGER DEFAULT 0",
                "created_at DATETIME",
            ],
            "user_xp": [
                "xp_points INTEGER DEFAULT 0",
                "level INTEGER DEFAULT 1",
            ],
            "user_badges": [
                "user_id INTEGER",
                "badge_name TEXT",
                "awarded_at DATETIME",
            ],
        }

        for table_name, columns in expected_columns.items():
            if not _table_exists(conn, table_name):
                continue

            existing = _get_columns(conn, table_name)
            for col_def in columns:
                col_name = col_def.split(" ", 1)[0]
                if col_name not in existing:
                    conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_def}")

        # Compatibility for older password_hash naming.
        if _table_exists(conn, "users"):
            user_cols = _get_columns(conn, "users")
            if "password" not in user_cols and "password_hash" in user_cols:
                conn.execute("ALTER TABLE users ADD COLUMN password TEXT")
                conn.execute(
                    "UPDATE users SET password = password_hash "
                    "WHERE (password IS NULL OR password = '') AND password_hash IS NOT NULL"
                )

            # Backfill missing referral codes.
            user_cols = _get_columns(conn, "users")
            if "referral_code" in user_cols:
                rows = conn.execute(
                    "SELECT id, name, referral_code FROM users"
                ).fetchall()
                existing_codes = {row[2] for row in rows if row[2]}
                for user_id, name, referral_code in rows:
                    if not referral_code:
                        code = _build_referral_code(name, user_id, existing_codes)
                        conn.execute(
                            "UPDATE users SET referral_code = ? WHERE id = ?",
                            (code, user_id),
                        )

        # Backfill missing or blank course status.
        if _table_exists(conn, "courses"):
            course_cols = _get_columns(conn, "courses")
            if "status" in course_cols:
                conn.execute(
                    "UPDATE courses SET status = 'draft' "
                    "WHERE status IS NULL OR TRIM(status) = ''"
                )

        if _table_exists(conn, "quiz_questions"):
            qq_cols = _get_columns(conn, "quiz_questions")
            if "order_index" in qq_cols and "order_number" in qq_cols:
                conn.execute(
                    "UPDATE quiz_questions SET order_index = COALESCE(order_number, order_index, 1)"
                )

        if _table_exists(conn, "enrollments"):
            enroll_cols = _get_columns(conn, "enrollments")
            if "progress_percentage" in enroll_cols and "progress" in enroll_cols:
                conn.execute(
                    "UPDATE enrollments SET progress_percentage = COALESCE(progress_percentage, progress, 0.0)"
                )

        if _table_exists(conn, "quiz_attempts"):
            qa_cols = _get_columns(conn, "quiz_attempts")
            if "start_time" in qa_cols:
                conn.execute(
                    "UPDATE quiz_attempts SET start_time = COALESCE(start_time, started_at, CURRENT_TIMESTAMP)"
                )
            if "end_time" in qa_cols:
                conn.execute(
                    "UPDATE quiz_attempts SET end_time = COALESCE(end_time, submitted_at, started_at)"
                )

        if _table_exists(conn, "admin_users"):
            admin_cols = _get_columns(conn, "admin_users")
            if "role" in admin_cols:
                conn.execute(
                    "UPDATE admin_users SET role = 'super_admin' "
                    "WHERE role IS NULL OR TRIM(role) = ''"
                )
            if "password_changed_at" in admin_cols:
                conn.execute(
                    "UPDATE admin_users SET password_changed_at = CURRENT_TIMESTAMP "
                    "WHERE password_changed_at IS NULL"
                )

        conn.commit()


# Create database tables and seed default admin user
@app.before_request
def before_request():
    """Run before each request"""

@app.context_processor
def inject_user():
    """Make user available in templates"""
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    csrf_token = session.get('csrf_token')
    if not csrf_token:
        csrf_token = secrets.token_urlsafe(32)
        session['csrf_token'] = csrf_token
    return dict(current_user=user, csrf_token=csrf_token)

# ============================================
# HARDCODED AI CHATBOT API ROUTE
# ============================================

@app.route("/api/chatbot/ask", methods=["POST"])
def chatbot_ask():
    """
    Rule-based Chatbot API Endpoint
    Handles student questions with page-aware, offline logic.
    
    Request body:
    {
        "question": "What is Python?",
        "context": {
            "page": "homepage|course|domain",
            "course": "Course Name",
            "domain": "Domain Name"
        }
    }
    
    Response:
    {
        "success": true,
        "answer": "Python is..."
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request format"
            }), 400
        
        question = data.get("question", "").strip()
        context = data.get("context")
        
        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty"
            }), 400
        
        if not isinstance(context, dict):
            context = {}
        if 'user_id' not in context and 'user_id' in session:
            context['user_id'] = session.get('user_id')

        from services.ai.rulebased_chatbot_service import build_rulebased_chatbot_payload
        payload = build_rulebased_chatbot_payload(
            question,
            context=context,
            user_id=session.get('user_id'),
        )
        answer = payload.get("answer", "")
        options = payload.get("options", [])
        response_data = {
            "success": True,
            "data": {
                "answer": answer,
                "agent": payload.get("agent", "rulebased_mentor"),
                "options": options,
                "suggestions": options,
            },
            "answer": answer,
            "response": answer,
            "options": options,
            "agent": payload.get("agent", "rulebased_mentor"),
            "suggestions": options,
            "deprecated": True,
            "deprecated_in_favor_of": "/api/chat",
        }

        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error in chatbot API: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred processing your question"
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    print(f"Internal server error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400

# Create application context and initialize database
with app.app_context():
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        db_path = os.path.join(app.instance_path, 'portal.db')
        _repair_legacy_schema(db_path)
    db.create_all()
    try:
        from backend.models import ensure_privacy_schema
        ensure_privacy_schema(db.session)
    except Exception:
        pass
    _sync_course_image_references()

    try:
        db.session.execute(text('SELECT 1'))
        if use_mysql:
            print('MySQL connection successful')
        else:
            print('SQLite connection successful')
    except Exception as e:
        print('Database connection failed:', e)

    try:
        if use_mysql:
            db_name_row = db.session.execute(text('SELECT DATABASE()')).fetchone()
            db_name = db_name_row[0] if db_name_row else None
            print('Connected to database:', db_name)

            print('Tables in database:')
            for table in db.session.execute(text('SHOW TABLES')):
                print('-', table[0])

            user_count_row = db.session.execute(text('SELECT COUNT(*) FROM users')).fetchone()
            user_count = user_count_row[0] if user_count_row else 0
            print('Total users:', user_count)
    except Exception as e:
        print('Database inspection failed:', e)

    # Create default admin user if it doesn't exist
    admin_user = User.query.filter_by(email='admin@eduportal.com').first()
    if not admin_user:
        admin = User(
            name='Admin User',
            email='admin@eduportal.com',
            role='admin',
            referral_code=f"TEMP{secrets.token_hex(4).upper()}"
        )
        default_admin_password = os.environ.get("DEFAULT_ADMIN_PASSWORD")
        if not default_admin_password:
            raise RuntimeError("DEFAULT_ADMIN_PASSWORD environment variable is required")
            
        admin.set_password(default_admin_password)
        db.session.add(admin)
        db.session.flush()
        admin.referral_code = admin.generate_referral_code()

        # Create AdminUser profile
        admin_profile = AdminUser(
            user_id=admin.id,
            username='admin',
            full_name='Admin User',
            email='admin@eduportal.com',
            role='super_admin',
        )
        admin_profile.set_password(default_admin_password)
        db.session.add(admin_profile)
        db.session.commit()
        print('Default admin user created successfully')

if __name__ == '__main__':
    import os
    if os.environ.get('MENTRA_ENV') == 'development':
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        try:
            from waitress import serve
            print("\n=======================================================")
            print("Starting Mentra Platform with Waitress WSGI server")
            print("Listening on http://127.0.0.1:5000")
            print("Press CTRL+C to quit (Note: Dev-mode auto-reload is off)")
            print("=======================================================\n")
            serve(app, host='127.0.0.1', port=5000)
        except ImportError:
            print("Waitress not installed. Falling back to development server...")
            app.run(debug=True, host='127.0.0.1', port=5000)










