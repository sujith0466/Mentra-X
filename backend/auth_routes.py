from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from backend.models import db, User, ReferralTransaction, AdminUser, UserResume
from backend.services.ai.career.resume_parser_service import extract_text_from_docx, extract_text_from_pdf, parse_resume
from backend.services.twin.twin_initializer import TwinInitializationService
from datetime import datetime, timezone
from backend.audit_utils import log_audit
import re
import time
import uuid
import json
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
LOGIN_WINDOW_SECONDS = 300
LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 600
_LOGIN_ATTEMPTS = {}
RESUME_UPLOAD_DIR = os.path.join("uploads", "resumes")
ALLOWED_RESUME_EXTENSIONS = {".pdf", ".docx"}

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False
    return True


def generate_referral_code():
    """Generate a unique referral code for new users."""
    while True:
        code = str(uuid.uuid4()).replace('-', '')[:8].upper()
        if not User.query.filter_by(referral_code=code).first():
            return code


def _is_rate_limited(client_key):
    now = time.time()
    entry = _LOGIN_ATTEMPTS.get(client_key, {"attempts": [], "locked_until": 0})
    if entry["locked_until"] > now:
        return True, int(entry["locked_until"] - now)
    entry["attempts"] = [ts for ts in entry["attempts"] if now - ts <= LOGIN_WINDOW_SECONDS]
    _LOGIN_ATTEMPTS[client_key] = entry
    return False, 0


def _record_failed_attempt(client_key):
    now = time.time()
    entry = _LOGIN_ATTEMPTS.get(client_key, {"attempts": [], "locked_until": 0})
    entry["attempts"] = [ts for ts in entry["attempts"] if now - ts <= LOGIN_WINDOW_SECONDS]
    entry["attempts"].append(now)
    if len(entry["attempts"]) >= LOGIN_MAX_ATTEMPTS:
        entry["locked_until"] = now + LOGIN_LOCKOUT_SECONDS
    _LOGIN_ATTEMPTS[client_key] = entry


def _clear_attempts(client_key):
    if client_key in _LOGIN_ATTEMPTS:
        del _LOGIN_ATTEMPTS[client_key]


def _save_resume_upload(file_storage, user_id: int) -> tuple[str, dict]:
    if not file_storage or not file_storage.filename:
        return "", {}
    _, extension = os.path.splitext(file_storage.filename)
    extension = extension.lower()
    if extension not in ALLOWED_RESUME_EXTENSIONS:
        return "", {}

    os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)
    safe_name = secure_filename(file_storage.filename) or f"resume_{user_id}{extension}"
    unique_name = f"{os.path.splitext(safe_name)[0]}_{uuid.uuid4().hex[:8]}{extension}"
    relative_path = os.path.join("resumes", unique_name)
    save_path = os.path.join(RESUME_UPLOAD_DIR, unique_name)
    file_storage.save(save_path)

    extracted_text = ""
    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(save_path)
    elif extension == ".docx":
        extracted_text = extract_text_from_docx(save_path)

    parsed = parse_resume(extracted_text or "")
    return relative_path, parsed

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Student Registration"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        referral_code = (request.form.get('referral_code') or '').strip()
        if not referral_code:
            referral_code = (session.get('referral_code') or '').strip()
        
        # Validation
        if not all([name, email, password, confirm_password]):
            flash('Please fill in all required fields!', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(name) < 2 or len(name) > 100:
            flash('Name must be between 2 and 100 characters!', 'danger')
            return redirect(url_for('auth.register'))
        
        if not is_valid_email(email):
            flash('Please enter a valid email address!', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered! Please login or use a different email.', 'danger')
            return redirect(url_for('auth.register'))
        
        if not is_valid_password(password):
            flash('Password must be at least 6 characters long!', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.register'))
        
        try:
            # Check if referral code is valid
            referred_by_user = None
            if referral_code:
                referred_by_user = User.query.filter_by(referral_code=referral_code).first()
                if not referred_by_user:
                    session.pop('referral_code', None)
                    flash('Invalid referral code!', 'danger')
                    return redirect(url_for('auth.register'))
                if referred_by_user.email == email:
                    session.pop('referral_code', None)
                    flash('You cannot use your own referral code.', 'danger')
                    return redirect(url_for('auth.register'))
            
            # Create new user
            new_user = User(
                name=name,
                email=email,
                role='student',
                referral_code=generate_referral_code(),
                referred_by=referral_code if referral_code else None,
                wallet_balance=0.0,
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.flush()  # To get the user ID before commit

            resume_file = request.files.get("resume")
            if resume_file and resume_file.filename:
                resume_path, parsed = _save_resume_upload(resume_file, new_user.id)
                if resume_path:
                    resume_entry = UserResume(
                        user_id=new_user.id,
                        resume_path=resume_path,
                        skills_json=json.dumps(parsed.get("skills", [])),
                        projects_json=json.dumps(parsed.get("projects", [])),
                        education_json=json.dumps(parsed.get("education", [])),
                        experience_json=json.dumps(parsed.get("experience", [])),
                    )
                    db.session.add(resume_entry)
            
            # Process referral reward if applicable
            if referred_by_user:
                # Give referral bonus to both users
                referred_by_user.wallet_balance += 100
                new_user.wallet_balance += 100
                
                # Create referral transaction
                referral_tx = ReferralTransaction(
                    referrer_id=referred_by_user.id,
                    new_user_id=new_user.id,
                    reward_amount=100.0
                )
                db.session.add(referral_tx)
            
            db.session.commit()
            flash(f'Registration successful! Your referral code is: {new_user.referral_code}', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")
            flash('Error during registration. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    
    # GET request - get referral code from URL if provided
    referral_code = request.args.get('ref', '') or session.get('referral_code', '')
    return render_template('auth/register.html', referral_code=referral_code)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User Login (Student & Admin)"""
    if request.method == 'POST':
        client_key = request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown')
        limited, remaining = _is_rate_limited(client_key)
        if limited:
            log_audit(entity_type='security', action_type='rate_limit', metadata={'email': request.form.get('email', '')})
            flash(f'Too many login attempts. Try again in {remaining} seconds.', 'danger')
            return redirect(url_for('auth.login'))

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not all([email, password]):
            _record_failed_attempt(client_key)
            flash('Please enter email and password!', 'danger')
            return redirect(url_for('auth.login'))
        
        try:
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                _clear_attempts(client_key)
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_role'] = user.role
                session['user_email'] = user.email
                
                flash(f'Welcome back, {user.name}!', 'success')
                
                # Redirect based on user role
                if user.role == 'admin':
                    admin_profile = AdminUser.query.filter_by(user_id=user.id).first()
                    if admin_profile:
                        session['admin_role'] = admin_profile.role or 'super_admin'
                        admin_profile.last_login = datetime.utcnow()
                        db.session.commit()
                    else:
                        session['admin_role'] = 'super_admin'
                    session['admin_last_seen'] = datetime.utcnow().isoformat()
                    log_audit(
                        entity_type='auth',
                        action_type='admin_login',
                        entity_id=user.id,
                        actor_id=user.id,
                        actor_role=session.get('admin_role', 'super_admin'),
                        metadata={'email': user.email},
                    )
                    return redirect(url_for('admin.dashboard'))
                else:
                    try:
                        # Milestone 4: Lazy Twin Initialization
                        TwinInitializationService.ensure_twin(user.id)
                    except Exception as e:
                        print(f"Failed to initialize twin for user {user.id}: {e}")
                        # Even if twin fails, allow login to proceed
                        
                    return redirect(url_for('student.dashboard'))
            else:
                _record_failed_attempt(client_key)
                flash('Invalid email or password!', 'danger')
                return redirect(url_for('auth.login'))
        
        except Exception as e:
            _record_failed_attempt(client_key)
            print(f"Error during login: {e}")
            flash('An error occurred during login. Please try again.', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """User Logout"""
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('public.index'))
