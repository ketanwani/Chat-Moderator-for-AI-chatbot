# Setup Guide

This guide will help you set up and run the Real-Time Moderation and Compliance Engine.

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL 13 or higher
- Git

## Step 1: Database Setup

### Install PostgreSQL

**Windows:**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer and set a password for the postgres user
3. Keep the default port (5432)

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE moderation_db;

# Exit psql
\q
```

## Step 2: Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` file with your database credentials:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/moderation_db
SECRET_KEY=your-secret-key-change-in-production
ML_MODEL_CACHE_DIR=./model_cache
LOG_LEVEL=INFO
```

### 5. Initialize database with seed data
```bash
python init_db.py
```

### 6. Run the backend server
```bash
# Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python main.py
```

The backend API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## Step 3: Frontend Setup

### 1. Open a new terminal and navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Start the development server
```bash
npm start
```

The frontend will be available at: http://localhost:3000

## Step 4: Verify Installation

### Test the Backend API

1. Open http://localhost:8000/docs
2. Try the `/health` endpoint - should return `{"status": "healthy"}`
3. Test the `/api/v1/admin/rules` endpoint - should return the seed rules

### Test the Frontend

1. Open http://localhost:3000
2. Try sending a message in the chat interface
3. Switch to the Admin Panel to view rules and statistics

## Default Configuration

The system comes pre-configured with the following rules:

1. **Global Toxicity Detection** - Detects toxic, offensive content
2. **Global PII Detection** - Detects personally identifiable information
3. **US HIPAA Medical Terms** - Blocks medical diagnosis information (US only)
4. **EU GDPR Data Protection** - Enhanced PII detection (EU only)
5. **Restricted Financial Advice** - Blocks specific investment advice
6. **Hate Speech Keywords** - Blocks known hate speech terms
7. **Cryptocurrency Scam Detection** - Detects crypto scam patterns

## Testing the Moderation System

### Test PII Detection
Send a message like: "My email is john@example.com and my phone is 555-1234"
- The response should be blocked or flagged

### Test Toxicity Detection
Send a message with offensive language
- The response should be blocked with a fallback message

### Test Region-Specific Rules
1. Change region to "United States (HIPAA)"
2. Ask about medical conditions
3. Responses with medical terms should be moderated

## Troubleshooting

### Backend Issues

**Import Error: No module named 'app'**
- Make sure you're in the `backend` directory
- Ensure virtual environment is activated

**Database Connection Error**
- Check if PostgreSQL is running
- Verify credentials in `.env` file
- Ensure database `moderation_db` exists

**ML Model Download**
- First run will download ML models (Detoxify)
- This may take a few minutes
- Models are cached in `ML_MODEL_CACHE_DIR`

### Frontend Issues

**Cannot connect to backend**
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Ensure API_BASE_URL in components matches backend URL

**npm install errors**
- Try deleting `node_modules` and `package-lock.json`
- Run `npm install` again

## Performance Optimization

### Database
- Add indexes for frequently queried fields
- Use connection pooling in production

### ML Models
- Models are loaded once at startup
- Consider GPU acceleration for higher throughput
- Use Redis for caching moderation results

### API
- Enable response caching
- Use async processing for non-critical operations
- Monitor latency with the `/api/v1/admin/stats` endpoint

## Production Deployment

### Security
1. Change `SECRET_KEY` in `.env`
2. Use environment variables for all sensitive data
3. Enable HTTPS
4. Implement authentication for admin endpoints
5. Use PostgreSQL with SSL

### Scaling
1. Deploy multiple backend instances behind a load balancer
2. Use a managed PostgreSQL service (AWS RDS, Azure Database)
3. Consider Redis for distributed caching
4. Monitor performance metrics

### Monitoring
1. Set up logging aggregation (ELK, CloudWatch)
2. Monitor latency metrics (target: <100ms)
3. Set up alerts for high error rates
4. Track moderation statistics

## Next Steps

1. Customize moderation rules for your use case
2. Integrate with your actual chatbot/LLM system
3. Add authentication and authorization
4. Implement webhooks for rule updates
5. Add more sophisticated ML models
6. Set up automated testing

## Support

For issues or questions:
1. Check the API documentation at http://localhost:8000/docs
2. Review logs in the backend console
3. Check the audit logs in the Admin Panel

## Architecture Overview

```
┌─────────────┐
│   Frontend  │ (React)
│   Port 3000 │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │ (FastAPI)
│   Port 8000 │
└──────┬──────┘
       │
       ├──────► PostgreSQL (Rules, Audit Logs)
       │
       └──────► ML Models (Detoxify, SpaCy)
```

## API Endpoints Summary

### Chat API
- `POST /api/v1/chat` - Send chat message with moderation

### Admin API
- `GET /api/v1/admin/rules` - Get all rules
- `POST /api/v1/admin/rules` - Create rule
- `PUT /api/v1/admin/rules/{id}` - Update rule
- `DELETE /api/v1/admin/rules/{id}` - Delete rule
- `GET /api/v1/admin/audit-logs` - Get audit logs
- `GET /api/v1/admin/stats` - Get statistics
