# Mentra X — Deployment Guide

**Owner:** Sujith Kumar AI  
**Version:** 1.0  

## 1. Deployment Environments
- **Development (Local):** `ENABLE_ALL=true`, SQLite or local MySQL, Dockerized Qdrant.
- **Staging:** Replicates production. Used for E2E tests and Judge Demos. Database is seeded with mock student data.
- **Production:** High availability. Redis caching enabled. Qdrant Cloud used instead of local Docker. Enkrypt AI set to strict mode.

## 2. Dependencies Checklist
Before deploying to Staging or Production, ensure the following infrastructure is provisioned:
- [ ] MySQL 8.0+ Instance (RDS/Cloud SQL)
- [ ] MongoDB Atlas Instance (for audit logs)
- [ ] Qdrant Cloud Cluster (or self-hosted Qdrant server)
- [ ] Redis ElastiCache (for Twin caching)
- [ ] OpenAI API Key (GPT-4o)
- [ ] Enkrypt AI API Key

## 3. Docker Deployment (Recommended)

**Step 1: Environment Setup**
Create a `.env.production` file on the deployment server:
```bash
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://user:pass@host:3306/mentrax
MONGO_URI=mongodb+srv://...
QDRANT_HOST=https://xxx.qdrant.tech
QDRANT_API_KEY=...
OPENAI_API_KEY=...
ENKRYPT_API_KEY=...
ENABLE_ALL=true
```

**Step 2: docker-compose.yml**
```yaml
version: '3.8'
services:
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:5000 run:app --workers 4 --threads 2
    ports:
      - "5000:5000"
    env_file:
      - .env.production
    depends_on:
      - redis

  scheduler:
    build: .
    command: python -m backend.scheduler.jobs
    env_file:
      - .env.production

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

**Step 3: Build & Run**
```bash
docker-compose up -d --build
```

## 4. Manual Deployment (Without Docker)

For bare-metal Ubuntu servers:

**1. systemd Service (Web): `/etc/systemd/system/mentrax.service`**
```ini
[Unit]
Description=Gunicorn daemon for Mentra X
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/core
EnvironmentFile=/home/ubuntu/core/.env.production
ExecStart=/home/ubuntu/core/venv/bin/gunicorn --workers 4 --bind unix:mentrax.sock -m 007 run:app

[Install]
WantedBy=multi-user.target
```

**2. systemd Service (Scheduler): `/etc/systemd/system/mentrax-scheduler.service`**
```ini
[Unit]
Description=APScheduler for Mentra X background jobs
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/core
EnvironmentFile=/home/ubuntu/core/.env.production
ExecStart=/home/ubuntu/core/venv/bin/python -m backend.scheduler.jobs
Restart=always

[Install]
WantedBy=multi-user.target
```

**3. Nginx Configuration**
```nginx
server {
    listen 80;
    server_name api.mentrax.dev;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/core/mentrax.sock;
    }
}
```

## 5. Database Initialization
Run these commands ONCE on the production server after the first deployment:
```bash
# Initialize MySQL schemas
FLASK_ENV=production flask db upgrade

# Initialize Qdrant Collections
FLASK_ENV=production python scripts/init_qdrant.py

# Seed Super Admin
FLASK_ENV=production python scripts/seed_admin.py
```

## 6. Health Check Validation
After deployment, curl the health endpoint:
```bash
curl https://api.mentrax.dev/health
```
Expected output:
```json
{
  "status": "healthy",
  "checks": {
    "mysql": {"ok": true},
    "qdrant": {"ok": true},
    "redis": {"ok": true}
  }
}
```

## 7. Rollback Procedure
If a deployment fails or critical bugs are detected:
1. Revert to previous Git commit: `git checkout v1.0.4`
2. Restart services: `docker-compose restart` or `sudo systemctl restart mentrax`
3. If database migrations were run, roll them back: `flask db downgrade`
4. Do NOT attempt to manually roll back Qdrant vectors unless absolutely necessary (Twin Mutator will auto-correct minor discrepancies on the next run).

## 8. Zero-Downtime Deployment
Mentra X relies on Gunicorn for zero-downtime reloads. When code is pushed:
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo systemctl reload mentrax  # Reloads workers gracefully
```
Background jobs (Scheduler) should be restarted entirely: `sudo systemctl restart mentrax-scheduler`
