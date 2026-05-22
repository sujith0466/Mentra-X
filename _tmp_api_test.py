import sys, json
from app import app, db
import traceback

def test_routes():
    test_client = app.test_client()
    output = []
    
    # 1. Feature 9: Flashcards
    output.append('--- Testing POST /api/flashcards ---')
    r1 = test_client.post('/api/flashcards', json={
        'notes_text': "Python is a high-level programming language. Variable - A container that stores data."
    })
    output.append(f"Status: {r1.status_code}")
    output.append(f"JSON: {json.dumps(r1.get_json())}")
    
    # 2. Feature 10: Doubt Solver
    output.append('\n--- Testing POST /api/doubt-solver ---')
    r2 = test_client.post('/api/doubt-solver', json={
        'question_text': "What is a python loop?"
    })
    output.append(f"Status: {r2.status_code}")
    output.append(f"JSON: {json.dumps(r2.get_json())}")
    
    # 3. Feature 11: Study Planner
    output.append('\n--- Testing GET /api/study-plan ---')
    with test_client.session_transaction() as sess:
        sess['user_id'] = 1
    r3 = test_client.get('/api/study-plan')
    output.append(f"Status: {r3.status_code}")
    output.append(f"JSON: {json.dumps(r3.get_json())}")
    
    # 4. Feature 12: Streak
    output.append('\n--- Testing GET /api/streak ---')
    try:
        r4 = test_client.get('/api/streak')
        output.append(f"Status: {r4.status_code}")
        output.append(f"JSON: {json.dumps(r4.get_json())}")
    except Exception as e:
        output.append(f"Error: {e}")

    # 4. Feature 12: XP
    output.append('\n--- Testing GET /api/xp ---')
    try:
        r5 = test_client.get('/api/xp')
        output.append(f"Status: {r5.status_code}")
        output.append(f"JSON: {json.dumps(r5.get_json())}")
    except Exception as e:
        output.append(f"Error: {e}")
        
    with open('_tmp_test_output.txt', 'w') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    with app.app_context():
        test_routes()
