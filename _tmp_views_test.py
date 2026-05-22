import sys
from app import app

def test_routes():
    test_client = app.test_client()
    output = []
    
    with test_client.session_transaction() as sess:
        sess['user_id'] = 1  # Provide session so user is logged in
        
    routes_to_test = [
        '/dashboard/overview',
        '/student/learning-path',
        '/student/weekly-report',
        '/student/flashcards',
        '/student/doubt-solver',
        '/student/resume-improver'
    ]
    
    for route in routes_to_test:
        r = test_client.get(route)
        output.append(f"Testing {route}: Status {r.status_code}")
        
    with open('_tmp_views_test_output.txt', 'w') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    with app.app_context():
        test_routes()
