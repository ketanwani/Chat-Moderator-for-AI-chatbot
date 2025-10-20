# Real-Time Moderation and Compliance Engine

A backend service that moderates AI chatbot responses in real-time to enforce content compliance rules.

## Architecture

![System Architecture](assets/images/architecture.png)

*Complete system architecture showing the moderation engine with 100% response interception, ML-based detection, and comprehensive monitoring.*

## Features

- **Real-time moderation**: Intercepts all chatbot responses before delivery (100%)
- **ML-based detection**: Integrates toxicity and PII detection models
- **Region-specific rules**: GDPR, HIPAA, and custom compliance rules
- **Dynamic configuration**: Update rules without redeployment
- **Audit logging**: Complete audit trail for compliance (flagged responses only)
- **Dynamic LLM selection**: Choose between Mock, OpenAI, Anthropic providers
- **Monitoring**: Prometheus + Grafana dashboards with real-time metrics

## Tech Stack

- **Backend**: Python FastAPI, PostgreSQL
- **Frontend**: React.js
- **ML Models**: HuggingFace Transformers (Detoxify, SpaCy)

## Data Model

![Data Model](assets/images/data%20model.png)

*Database schema showing moderation_rules and audit_logs tables with their relationships and key fields.*

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

## Running Tests 🧪

> **Note:** Tests run inside Docker - no local Python installation required!

### Quick Test Commands

**Windows:**
```bash
run_tests.bat
```

**Linux/Mac:**
```bash
./run_tests.sh
```

**Or use Docker directly:**
```bash
# Run all 35 tests
docker exec moderation_backend python -m pytest tests/ -v

# Run with coverage report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=term-missing
```

### Test Coverage

```
✅ 35 tests - 100% passing
✅ 66% code coverage
✅ All critical paths tested
```

**Test Breakdown:**
- Core moderation logic: 8 tests
- ML detection (PII, toxicity, etc.): 12 tests
- Chatbot service: 8 tests
- API endpoints: 7 tests

For detailed testing documentation, see [backend/TESTING.md](backend/TESTING.md)

---

## Environment Variables

Create a `.env` file in the backend directory:

```
DATABASE_URL=postgresql://user:password@localhost:5432/moderation_db
SECRET_KEY=your-secret-key
ML_MODEL_CACHE_DIR=./model_cache
LLM_PROVIDER=mock  # Options: mock, openai, anthropic
```

## Monitoring & Metrics

The system includes comprehensive monitoring via Prometheus and Grafana:

### Access Monitoring
- **Grafana Dashboard**: http://localhost:3001 (default credentials: `admin/admin`)
- **Prometheus**: http://localhost:9090
- **Backend Metrics**: http://localhost:8000/metrics

### Available Metrics
- Request counts and rates
- Moderation latency (P50, P95, P99)
- Flagged/blocked response rates
- False Positive Rate (FPR) tracking
- Active rules and detection rates

### False Positive Rate Testing

Run the FPR test suite to validate moderation accuracy:

**Windows:**
```bash
run_fpr_tests.bat
```

**Linux/Mac:**
```bash
./run_fpr_tests.sh
```

**With metrics update:**
```bash
run_fpr_tests.bat --update-metrics
```

Results are saved to `backend/test_results/` with detailed confusion matrix and performance metrics.

For more details, see [backend/FPR_TESTING.md](backend/FPR_TESTING.md)
