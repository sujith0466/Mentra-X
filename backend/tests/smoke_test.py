import time
import json
from backend.app import app
from backend.models import db, User

def measure(name, func, *args, **kwargs):
    t0 = time.time()
    res = func(*args, **kwargs)
    t1 = time.time()
    print(f"[{name}] latency: {(t1 - t0) * 1000:.2f} ms")
    return res

def run_smoke_test():
    print("=== Mentra AI Smoke Test & Performance Review ===")
    with app.test_client() as client:
        with app.app_context():
            user = User.query.filter_by(role='student').first()
            user_id = user.id
            email = user.email

        # 1. Login
        res = measure('Login', client.post, '/api/auth/login', json={'email': email, 'password': 'password123'})
        
        # We must set session directly since Mentra uses /auth/login for UI
        with client.session_transaction() as sess:
            sess['user_id'] = user_id
            sess['user_role'] = 'student'
            
        # 2. Twin Initialization / Dashboard
        res = measure('Twin Dashboard (Init)', client.get, '/api/v1/twin/dashboard')
        
        # 3. Assessment Start
        res = measure('Assessment Start', client.post, '/api/v1/assessment/start', json={'exam_track': 'JEE'})
        data_start = res.get_json()
        session_id = data_start.get('session_id')
        question_id = data_start.get('question', {}).get('id')
        current_diff = data_start.get('current_difficulty')

        # 4. Question Transitions
        res = measure('Question Transition (Answer)', client.post, '/api/v1/assessment/answer', json={
            'session_id': session_id,
            'question_id': question_id,
            'submitted_answer': "4",
            'current_difficulty': current_diff
        })

        # 5. Assessment Complete & Twin Update
        res = measure('Assessment Complete & Twin Update', client.post, '/api/v1/assessment/complete', json={'session_id': session_id})
        
        # 6. Twin Profile
        res = measure('Twin Profile Load', client.get, '/api/v1/twin/profile')
        
        print("Smoke test completed successfully!")

if __name__ == '__main__':
    run_smoke_test()
