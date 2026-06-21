# MongoDB Integration Task List

- `[x]` Create `task.md` to track progress
- `[x]` Append `pymongo` to `requirements.txt`
- `[x]` Append MongoDB configuration variables to `.env`
- `[x]` Create `services/mongo_service.py` with safe helpers (`get_mongo_db`, `get_collections`, `safe_insert`)
- `[x]` Modify `app.py` to initialize MongoDB, bind to app context, and add `/mongo-check` route
- `[x]` Modify `app.py` `/api/chatbot/ask` route to log to `chat_logs` using `safe_insert`
- `[x]` Modify `ai_routes.py` `resume_analyzer` route to log to `learning_insights`
- `[x]` Modify `ai_routes.py` `project_generate` route to log to `project_ideas` collection
- `[x]` Modify `ai_routes.py` coding submission routes to log to `coding_logs` collection
- `[x]` Update `README.md`
- `[x]` Update `Docs/DEPLOYMENT_GUIDE.md`
