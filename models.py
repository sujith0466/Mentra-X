from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import string
import random
import json

db = SQLAlchemy()

# User Model (Students & Admins)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')  # 'student' or 'admin'
    referral_code = db.Column(db.String(20), unique=True, nullable=False)
    referred_by = db.Column(db.String(20), nullable=True)
    wallet_balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, foreign_keys='Enrollment.user_id')
    referral_transactions_as_referrer = db.relationship('ReferralTransaction', backref='referrer', lazy=True, foreign_keys='ReferralTransaction.referrer_id')
    referral_transactions_as_new_user = db.relationship('ReferralTransaction', backref='new_user', lazy=True, foreign_keys='ReferralTransaction.new_user_id')
    resume = db.relationship('UserResume', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_referral_code(self):
        """Generate unique referral code"""
        base_code = (self.name.upper().replace(' ', '')[:6]) + str(self.id)
        return base_code[:12]
    
    def __repr__(self):
        return f'<User {self.name}>'


class UserResume(db.Model):
    __tablename__ = 'user_resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    resume_path = db.Column(db.String(500), nullable=True)
    skills_json = db.Column(db.Text, nullable=True)
    projects_json = db.Column(db.Text, nullable=True)
    education_json = db.Column(db.Text, nullable=True)
    experience_json = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserResume {self.user_id}>'


# Domain Model
class Domain(db.Model):
    __tablename__ = 'domains'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # Path to domain image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    courses = db.relationship('Course', backref='domain', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Domain {self.name}>'


# Course Model
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False)
    price = db.Column(db.Float, default=0.0)
    instructor = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    demo_video_url = db.Column(db.String(500), nullable=True)  # YouTube/Vimeo embed URL
    status = db.Column(db.String(20), nullable=False, default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    syllabuses = db.relationship('Syllabus', backref='course', lazy=True, cascade='all, delete-orphan')
    videos = db.relationship('Video', backref='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='course', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='course', lazy=True, cascade='all, delete-orphan')
    lesson_progresses = db.relationship('LessonProgress', backref='course', lazy=True, cascade='all, delete-orphan')
    modules = db.relationship('CourseModule', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.title}>'


# Syllabus Model
class Syllabus(db.Model):
    __tablename__ = 'syllabuses'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    topic_title = db.Column(db.String(200), nullable=False)
    topic_description = db.Column(db.String(1000), nullable=True)
    order_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Syllabus {self.topic_title}>'


# Video Model
class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    duration = db.Column(db.String(20), nullable=True)  # e.g., "45:30"
    module_id = db.Column(db.Integer, db.ForeignKey('course_modules.id'), nullable=True, index=True)
    order_number = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Video {self.title}>'


# Enrollment Model
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_date = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Float, default=0.0)  # 0-100 percentage
    progress_percentage = db.Column(db.Float, default=0.0)  # Cached progress
    completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Enrollment {self.user_id}-{self.course_id}>'


# Contact Messages Model
class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.name}>'


# Referral Transactions Model
class ReferralTransaction(db.Model):
    __tablename__ = 'referral_transactions'
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    new_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reward_amount = db.Column(db.Float, default=100.0)
    status = db.Column(db.String(20), default='completed')  # 'pending' or 'completed'
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ReferralTransaction {self.referrer_id}-{self.new_user_id}>'


# AI Chatbot Conversation Model
class ChatbotConversation(db.Model):
    __tablename__ = 'chatbot_conversations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Allow anonymous
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)  # Optional: track course context
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    domain = db.Column(db.String(100), nullable=True)  # Domain context (Web Dev, Data Science, etc.)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatbotConversation {self.user_id}-{self.timestamp}>'


# Admin Management Model
class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(30), nullable=False, default='super_admin')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    password_changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='admin_profile')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<AdminUser {self.username}>'


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.Integer, nullable=True)
    action_type = db.Column(db.String(50), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    actor_role = db.Column(db.String(30), nullable=True)
    before_values = db.Column(db.Text, nullable=True)
    after_values = db.Column(db.Text, nullable=True)
    metadata_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    actor = db.relationship('User', backref='audit_logs')

    @staticmethod
    def _to_json(value):
        if value is None:
            return None
        try:
            return json.dumps(value, default=str)
        except Exception:
            return None

    def set_before(self, value):
        self.before_values = self._to_json(value)

    def set_after(self, value):
        self.after_values = self._to_json(value)

    def set_metadata(self, value):
        self.metadata_json = self._to_json(value)

    def __repr__(self):
        return f'<AuditLog {self.entity_type}:{self.action_type}>'


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    question_count_target = db.Column(db.Integer, nullable=False, default=10)
    passing_percentage = db.Column(db.Float, nullable=False, default=60.0)
    time_limit_minutes = db.Column(db.Integer, nullable=False, default=15)
    attempts_allowed = db.Column(db.Integer, nullable=False, default=3)
    is_enabled = db.Column(db.Boolean, nullable=False, default=True)
    module_id = db.Column(db.Integer, db.ForeignKey('course_modules.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Quiz {self.title}>'


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(30), nullable=False, default='mcq')  # mcq, true_false, short_answer, long_answer
    option_a = db.Column(db.String(500), nullable=True)
    option_b = db.Column(db.String(500), nullable=True)
    option_c = db.Column(db.String(500), nullable=True)
    option_d = db.Column(db.String(500), nullable=True)
    correct_answer = db.Column(db.String(500), nullable=False)
    order_index = db.Column(db.Integer, nullable=False, default=1)
    order_number = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    answers = db.relationship('QuizAnswer', backref='question', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<QuizQuestion {self.id}:{self.question_type}>'


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    attempt_number = db.Column(db.Integer, nullable=False, default=1)
    total_questions = db.Column(db.Integer, nullable=False, default=0)
    correct_answers = db.Column(db.Integer, nullable=False, default=0)
    score_percentage = db.Column(db.Float, nullable=False, default=0.0)
    passed = db.Column(db.Boolean, nullable=False, default=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship('User', backref='quiz_attempts')
    answers = db.relationship('QuizAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<QuizAttempt {self.id}:{self.user_id}:{self.quiz_id}>'


class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answers'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False, index=True)
    submitted_answer = db.Column(db.Text, nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<QuizAnswer {self.id}:{self.attempt_id}>'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    marks = db.Column(db.Float, nullable=False, default=100.0)
    module_id = db.Column(db.Integer, db.ForeignKey('course_modules.id'), nullable=True, index=True)
    attachment_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    submissions = db.relationship('AssignmentSubmission', backref='assignment', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Assignment {self.title}>'


class AssignmentSubmission(db.Model):
    __tablename__ = 'assignment_submissions'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    answer_text = db.Column(db.Text, nullable=True)
    submission_file = db.Column(db.String(500), nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    marks_awarded = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.String(1000), nullable=True)
    graded_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship('User', backref='assignment_submissions')

    def __repr__(self):
        return f'<AssignmentSubmission {self.id}:{self.user_id}>'


class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship('User', backref='lesson_progresses')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_id', name='uq_lesson_progress_user_lesson'),
    )

    def __repr__(self):
        return f'<LessonProgress {self.user_id}:{self.lesson_id}>'


class LearningStreak(db.Model):
    __tablename__ = 'learning_streaks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    last_learning_date = db.Column(db.Date, nullable=True)
    current_streak = db.Column(db.Integer, nullable=False, default=0)
    longest_streak = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship('User', backref='learning_streak', uselist=False)

    def __repr__(self):
        return f'<LearningStreak {self.user_id}:{self.current_streak}>'



class SkillProgress(db.Model):
    __tablename__ = 'skill_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    skill_name = db.Column(db.String(200), nullable=False, index=True)
    progress_percentage = db.Column(db.Float, nullable=False, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship('User', backref='skill_progress_rows')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'skill_name', name='uq_skill_progress_user_skill'),
    )

    def __repr__(self):
        return f'<SkillProgress {self.user_id}:{self.skill_name}:{self.progress_percentage}>'


class CodingChallenge(db.Model):
    __tablename__ = 'coding_challenges'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False, default='Beginner')
    topic = db.Column(db.String(100), nullable=False, index=True)
    starter_code = db.Column(db.Text, nullable=True)
    expected_output = db.Column(db.Text, nullable=True)
    test_cases_json = db.Column(db.Text, nullable=False, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    submissions = db.relationship('CodingSubmission', backref='challenge', lazy=True, cascade='all, delete-orphan')

    def get_test_cases(self):
        try:
            payload = json.loads(self.test_cases_json or '[]')
            return payload if isinstance(payload, list) else []
        except (TypeError, ValueError, json.JSONDecodeError):
            return []

    def __repr__(self):
        return f'<CodingChallenge {self.title}>'


class CodingSubmission(db.Model):
    __tablename__ = 'coding_submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('coding_challenges.id'), nullable=False, index=True)
    code_submitted = db.Column(db.Text, nullable=False)
    execution_output = db.Column(db.Text, nullable=True)
    passed_tests = db.Column(db.Integer, nullable=False, default=0)
    score = db.Column(db.Float, nullable=False, default=0.0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship('User', backref='coding_submissions')

    def __repr__(self):
        return f'<CodingSubmission {self.id}:{self.user_id}:{self.challenge_id}>'


class InterviewSession(db.Model):
    __tablename__ = 'interview_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role = db.Column(db.String(100), nullable=False, index=True)
    difficulty = db.Column(db.String(50), nullable=False, default='Beginner')
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(30), nullable=False, default='in_progress')

    student = db.relationship('User', backref='interview_sessions')
    questions = db.relationship('InterviewQuestion', backref='session', lazy=True, cascade='all, delete-orphan')
    responses = db.relationship('InterviewResponse', backref='session', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<InterviewSession {self.id}:{self.user_id}:{self.role}:{self.status}>'


class InterviewQuestion(db.Model):
    __tablename__ = 'interview_questions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('interview_sessions.id'), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False, default='technical')
    expected_answer = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(50), nullable=False, default='Beginner')

    responses = db.relationship('InterviewResponse', backref='question', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<InterviewQuestion {self.id}:{self.question_type}>'


class InterviewResponse(db.Model):
    __tablename__ = 'interview_responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('interview_sessions.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('interview_questions.id'), nullable=False, index=True)
    user_answer = db.Column(db.Text, nullable=True)
    ai_feedback = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f'<InterviewResponse {self.id}:{self.session_id}:{self.question_id}>'


class ProjectIdea(db.Model):
    __tablename__ = 'project_ideas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    domain = db.Column(db.String(100), nullable=False, index=True)
    difficulty = db.Column(db.String(50), nullable=False, default='Beginner')
    tech_stack = db.Column(db.Text, nullable=True)
    architecture = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student_projects = db.relationship('StudentProject', backref='project_idea', lazy=True, cascade='all, delete-orphan')

    def get_tech_stack_list(self):
        try:
            payload = json.loads(self.tech_stack or '[]')
            return payload if isinstance(payload, list) else []
        except (TypeError, ValueError, json.JSONDecodeError):
            return []

    def __repr__(self):
        return f'<ProjectIdea {self.title}>'


class StudentProject(db.Model):
    __tablename__ = 'student_projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_ideas.id'), nullable=False, index=True)
    progress_percentage = db.Column(db.Float, nullable=False, default=0.0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship('User', backref='student_projects')
    tasks = db.relationship('ProjectTask', backref='student_project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<StudentProject {self.id}:{self.user_id}:{self.project_id}>'


class ProjectTask(db.Model):
    __tablename__ = 'project_tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('student_projects.id'), nullable=False, index=True)
    task_title = db.Column(db.String(200), nullable=False)
    task_description = db.Column(db.Text, nullable=True)
    task_order = db.Column(db.Integer, nullable=False, default=1)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<ProjectTask {self.id}:{self.project_id}:{self.task_order}>'


class CommunityPost(db.Model):
    __tablename__ = 'community_posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    author = db.relationship('User', backref='community_posts')
    answers = db.relationship('CommunityAnswer', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CommunityPost {self.id}:{self.title}>'


class CommunityAnswer(db.Model):
    __tablename__ = 'community_answers'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    answer_text = db.Column(db.Text, nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    author = db.relationship('User', backref='community_answers')

    def __repr__(self):
        return f'<CommunityAnswer {self.id}:{self.post_id}:{self.user_id}>'


class UserXP(db.Model):
    __tablename__ = 'user_xp'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    xp_points = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)

    student = db.relationship('User', backref='xp_profile', uselist=False)

    def __repr__(self):
        return f'<UserXP {self.user_id}:{self.xp_points}:{self.level}>'


class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    badge_name = db.Column(db.String(100), nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship('User', backref='user_badges')

    def __repr__(self):
        return f'<UserBadge {self.user_id}:{self.badge_name}>'
class CourseModule(db.Model):
    __tablename__ = 'course_modules'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    order_index = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    lessons = db.relationship('Video', backref='module', lazy=True)
    quizzes = db.relationship('Quiz', backref='module', lazy=True)
    assignments = db.relationship('Assignment', backref='module', lazy=True)

    def __repr__(self):
        return f'<CourseModule {self.course_id}:{self.title}>'


