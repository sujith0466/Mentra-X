"""Test script for AI Chatbot API"""
import requests
import json

api_url = 'http://localhost:5000/api/chatbot'

# Test different queries
test_queries = [
    {'message': 'Explain Flask', 'domain': 'Web Development'},
    {'message': 'What is Machine Learning?', 'domain': 'Data Science'},
    {'message': 'Hello, how are you?', 'domain': 'General'},
    {'message': 'Thanks for your help!', 'domain': 'General'},
]

print('='*60)
print('🤖 CHATBOT TESTING - Multiple Queries')
print('='*60)

passed = 0
failed = 0

for i, query in enumerate(test_queries, 1):
    try:
        response = requests.post(api_url, json=query, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f'\n✅ Test {i}: {query["domain"]}')
                print(f'   Q: {query["message"]}')
                response_text = data.get('response', '')
                print(f'   A: {response_text[:65]}...')
                passed += 1
            else:
                print(f'❌ Test {i} API Error: {data.get("error")}')
                failed += 1
        else:
            print(f'❌ Test {i} HTTP Error: {response.status_code}')
            failed += 1
    except Exception as e:
        print(f'❌ Test {i} Error: {str(e)}')
        failed += 1

print('\n' + '='*60)
print(f'✅ PASSED: {passed}/{len(test_queries)} tests')
print(f'❌ FAILED: {failed}/{len(test_queries)} tests')
if failed == 0:
    print('✅ ALL CHATBOT TESTS PASSED!')
print('='*60)
