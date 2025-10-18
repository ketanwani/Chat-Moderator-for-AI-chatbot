# Real-Time Moderation and Compliance Engine

A backend service that moderates AI chatbot responses in real-time to enforce content compliance rules.

## Features

- **Real-time moderation**: Intercepts all chatbot responses before delivery
- **ML-based detection**: Integrates toxicity and PII detection models
- **Region-specific rules**: GDPR, HIPAA, and custom compliance rules
- **Dynamic configuration**: Update rules without redeployment
- **Audit logging**: Complete audit trail for compliance
- **High performance**: <100ms moderation latency

## Tech Stack

- **Backend**: Python FastAPI, PostgreSQL
- **Frontend**: React.js
- **ML Models**: HuggingFace Transformers (Detoxify, SpaCy)

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── middleware/
│   ├── alembic/
│   ├── requirements.txt
│   └── main.py
└── frontend/
    ├── src/
    ├── public/
    └── package.json
```

## Quick Start with Docker (Recommended) 🐳

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

### Start Everything with One Command

```bash
docker-compose up
```

That's it! The command will:
- ✅ Set up PostgreSQL database
- ✅ Build and start the backend (FastAPI)
- ✅ Build and start the frontend (React)
- ✅ Initialize database with seed data
- ✅ Configure networking between services

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Stop Services

```bash
docker-compose down
```

For detailed Docker instructions, see [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

---

## Alternative: Manual Setup

If you prefer not to use Docker:

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `POST /api/v1/chat` - Send chat message (with moderation)
- `GET /api/v1/admin/rules` - Get all moderation rules
- `POST /api/v1/admin/rules` - Create new rule
- `PUT /api/v1/admin/rules/{id}` - Update rule
- `DELETE /api/v1/admin/rules/{id}` - Delete rule
- `GET /api/v1/admin/audit-logs` - Get audit logs

## Environment Variables

Create a `.env` file in the backend directory:

```
DATABASE_URL=postgresql://user:password@localhost:5432/moderation_db
SECRET_KEY=your-secret-key
ML_MODEL_CACHE_DIR=./model_cache
```
