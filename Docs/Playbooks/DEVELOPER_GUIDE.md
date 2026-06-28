# Mentra X — Developer Guide

**Owner:** Sujith Kumar AI  
**Version:** 1.0  

## 1. Project Overview
Mentra X is a production-grade AI Student Digital Twin and Adaptive Learning Platform. 
It builds upon a legacy Flask/MySQL foundation (34 tables, standard LMS features) by adding a 6-agent Mastra orchestration layer, Qdrant vector memory, and Enkrypt AI safety validation.

## 2. Prerequisites
- Python 3.10+
- Node.js 18+ (for Mastra core)
- MySQL 8.0+
- MongoDB 6.0+ (for audit logs)
- Docker Desktop (optional, but recommended for local Qdrant/Redis)

## 3. First-Time Setup
```bash
# 1. Clone repository
git clone https://github.com/Mentra-X/core.git
cd core

# 2. Setup Virtual Environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Environment Variables
cp .env.example .env
# Edit .env and add your OpenAI, Enkrypt, and DB credentials.
# Set ENABLE_ALL=true if you want to bypass feature flags locally.

# 4. Database Setup
mysql -u root -p -e "CREATE DATABASE mentrax_dev;"
python scripts/init_db.py

# 5. Qdrant Setup (via Docker)
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
python scripts/init_qdrant.py
```

## 4. Running the Application
**Development Mode:**
```bash
flask run --debug --port=5000
```
**Scheduler (Run in separate terminal):**
```bash
python -m backend.scheduler.jobs
```

## 5. Adding a New API Endpoint
We strictly separate HTTP routing from business logic.

**Step 1: Define Route (e.g., `backend/routes/twin_routes.py`)**
```python
from flask import Blueprint, jsonify, request
from backend.services.twin_mutator import TwinMutator
from backend.dto.twin_dto import TwinMutationDTO

twin_bp = Blueprint('twin', __name__)

@twin_bp.route('/api/v1/twin/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id')
    service = TwinMutator()
    profile = service.get_profile(user_id)
    return jsonify({"success": True, "data": profile.to_dict()})
```

**Step 2: Define Service (e.g., `backend/services/twin_mutator.py`)**
```python
class TwinMutator:
    def get_profile(self, user_id: str) -> TwinDTO:
        # NO Flask imports here. Pure Python logic.
        record = db.query(...)
        return TwinDTO.from_db_record(record)
```

## 6. Adding a New Mastra Agent Tool
```python
from mastra.tools import AgentTool
from pydantic import BaseModel, Field

class CalculateDecayInput(BaseModel):
    mastery: float = Field(..., description="Current mastery 0-1")
    days_elapsed: int = Field(..., description="Days since last review")

class CalculateDecayTool(AgentTool):
    name = "calculate_decay"
    description = "Calculates Ebbinghaus forgetting curve"
    args_schema = CalculateDecayInput

    def _run(self, mastery: float, days_elapsed: int) -> float:
        retention = mastery * math.exp(-days_elapsed / 7.0)
        return round(retention, 2)
```

## 7. Adding a New Qdrant Collection
1. Add the collection name to `backend/services/memory/constants.py`
2. Update `scripts/init_qdrant.py`:
```python
client.create_collection(
    collection_name="new_collection",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)
```
3. Create the corresponding DTO in `backend/dto/`.

## 8. Debugging Guide

**How to debug Enkrypt failures?**
Check the MongoDB `agent_traces` collection. The trace will contain the exact `math_score`, `science_score`, and `failure_context` returned by Enkrypt before the hard fail was triggered.

**How to debug Mastra execution?**
Open the Developer Panel UI (`/admin/observability`) or look at the application logs for lines starting with `[MASTRA DAG] Node executed: ...`.

**How to debug background jobs?**
The scheduler logs are separate from the Flask app. Check the terminal running `scheduler/jobs.py` or the `mentra_scheduler.log` file.

## 9. Git Workflow
- **Branches:** `feature/phase-X-name`, `fix/issue-name`
- **Commits:** `[Phase-X] feat: added TwinHealth calc`
- **PRs:** Require 1 approval, passing unit tests, and no decrease in coverage.

## 10. Common Issues

| Symptom | Cause | Solution |
|---|---|---|
| `MEMORY_010` | Qdrant Docker container stopped | `docker start <container_id>` |
| 403 Forbidden | Missing admin role | Update user row in MySQL: `role='admin'` |
| "Digital Twin feature is not enabled" | Feature flag false | Set `ENABLE_DIGITAL_TWIN=true` in `.env` |
| `ENKRYPT_001` | API rate limit | Check Enkrypt dashboard, use fallback mock for dev |
