import json
from app import app

client = app.test_client()

def run_test():
    with client:
        print("=== TEST 1: Start Interview ===")
        resp1 = client.post('/api/interview/start', json={"role": "frontend"})
        data1 = json.loads(resp1.data)
        assert data1['status'] == 'success', f"Start failed: {data1}"
        assert len(data1['questions']) >= 3, "Should return at least 3 questions."
        print("PASS: Interview started successfully.")
        
        print("\n=== TEST 2: Submit Valid Answer ===")
        # Sending a good answer. "frontend" questions might include React, Virtual DOM, CSS Box model, etc.
        # We will just write a generalized good answer full of technical keywords to ensure a high score.
        good_answer = "The virtual DOM is a lightweight copy of the real DOM. React uses reconciliation and diffing to update the UI efficiently by changing only what is necessary in memory."
        resp2 = client.post('/api/interview/answer', json={"question_index": 0, "answer": good_answer})
        data2 = json.loads(resp2.data)
        assert data2['status'] == 'success', f"Answer failed: {data2}"
        print(f"PASS: Answer submitted. Score: {data2['result']['score']}/10")
        print(f"Feedback: {data2['result']['feedback']}")
        
        print("\n=== TEST 3: Submit Poor Answer ===")
        poor_answer = "I don't really know, maybe it's magic?"
        resp3 = client.post('/api/interview/answer', json={"question_index": 1, "answer": poor_answer})
        data3 = json.loads(resp3.data)
        print(f"PASS: Answer submitted. Score: {data3['result']['score']}/10")
        
        print("\n=== TEST 4: Session Safety (Out of Bounds) ===")
        resp_oob = client.post('/api/interview/answer', json={"question_index": 99, "answer": "test"})
        data_oob = json.loads(resp_oob.data)
        assert data_oob['status'] == 'error', "Should fail out of bounds."
        print("PASS: Handled out-of-bounds safety correctly.")
        
        print("\n=== TEST 5: Complete Interview ===")
        resp4 = client.post('/api/interview/complete')
        data4 = json.loads(resp4.data)
        assert data4['status'] == 'success', f"Complete failed: {data4}"
        summary = data4['summary']
        print(f"PASS: Interview completed.")
        print(f"Final Score: {summary['final_score']}")
        print(f"Questions Answered: {summary['total_answered']}/{summary['total_questions']}")
        
        print("\n=== TEST 6: Session Cleared ===")
        resp5 = client.post('/api/interview/complete')
        data5 = json.loads(resp5.data)
        assert data5['status'] == 'error', "Should fail because session is cleared."
        print("PASS: Session cleared successfully.")


if __name__ == '__main__':
    run_test()
