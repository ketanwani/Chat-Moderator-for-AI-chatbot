# Quick Reference Guide

## Quick Start Commands

### Start Everything (Windows)
```bash
start.bat
```

### Start Everything (macOS/Linux)
```bash
chmod +x start.sh
./start.sh
```

### Manual Start

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## Access URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

## API Quick Reference

### Chat API

**Send Message:**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!",
    "region": "global"
  }'
```

### Admin API

**Get All Rules:**
```bash
curl http://localhost:8000/api/v1/admin/rules
```

**Create Rule:**
```bash
curl -X POST http://localhost:8000/api/v1/admin/rules \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Rule",
    "rule_type": "keyword",
    "region": "global",
    "patterns": ["test"],
    "is_active": true,
    "priority": 50
  }'
```

**Update Rule:**
```bash
curl -X PUT http://localhost:8000/api/v1/admin/rules/1 \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

**Delete Rule:**
```bash
curl -X DELETE http://localhost:8000/api/v1/admin/rules/1
```

**Get Statistics:**
```bash
curl http://localhost:8000/api/v1/admin/stats
```

**Get Audit Logs:**
```bash
curl http://localhost:8000/api/v1/admin/audit-logs?limit=10
```

## Rule Types

| Type | Description | Example |
|------|-------------|---------|
| `pii` | Personal Identifiable Information | Email, phone, SSN |
| `toxicity` | Offensive content | ML-based detection |
| `hate_speech` | Hate speech | Specific patterns |
| `keyword` | Keyword matching | List of words |
| `regex` | Regex patterns | Complex patterns |
| `financial` | Financial terms | Investment advice |
| `medical` | Medical terms | HIPAA compliance |

## Regions

| Region | Code | Description |
|--------|------|-------------|
| Global | `global` | Applies everywhere |
| United States | `us` | HIPAA rules |
| European Union | `eu` | GDPR rules |
| United Kingdom | `uk` | UK-specific |
| Asia Pacific | `apac` | APAC-specific |

## Testing Scenarios

### Test PII Detection
**Message:** "My email is test@example.com"
**Expected:** Blocked/flagged

### Test Toxicity
**Message:** [offensive language]
**Expected:** Blocked with fallback

### Test Financial Terms
**Message:** "guaranteed investment returns"
**Expected:** Blocked with disclaimer

### Test Medical Terms (US Region)
**Message:** "tell me about my diagnosis"
**Expected:** Blocked with medical disclaimer

### Test Normal Message
**Message:** "What's the weather?"
**Expected:** Pass through normally

## Database Commands

### Connect to Database
```bash
psql -U postgres -d moderation_db
```

### View Rules
```sql
SELECT id, name, rule_type, region, is_active FROM moderation_rules;
```

### View Recent Logs
```sql
SELECT request_id, is_flagged, is_blocked, moderation_latency_ms
FROM audit_logs
ORDER BY timestamp DESC
LIMIT 10;
```

### Check Statistics
```sql
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN is_flagged THEN 1 ELSE 0 END) as flagged,
  SUM(CASE WHEN is_blocked THEN 1 ELSE 0 END) as blocked,
  AVG(moderation_latency_ms) as avg_latency
FROM audit_logs;
```

## Common Issues & Solutions

### Issue: Database connection error
**Solution:**
```bash
# Check PostgreSQL is running
# Windows: Services > PostgreSQL
# macOS: brew services list
# Linux: sudo systemctl status postgresql

# Verify credentials in backend/.env
DATABASE_URL=postgresql://postgres:password@localhost:5432/moderation_db
```

### Issue: ML model download slow
**Solution:**
- First run downloads Detoxify model (~500MB)
- Be patient, only happens once
- Models cached in `ML_MODEL_CACHE_DIR`

### Issue: Frontend can't connect to backend
**Solution:**
```bash
# Check backend is running on port 8000
curl http://localhost:8000/health

# Check CORS settings in backend/main.py
# Ensure frontend URL is in BACKEND_CORS_ORIGINS
```

### Issue: High latency (>100ms)
**Solution:**
1. Check database performance
2. Review ML model settings
3. Consider GPU acceleration
4. Add Redis caching

## File Locations

### Configuration
- Backend: `backend/.env`
- Frontend: `frontend/package.json`
- Database: Connection string in `.env`

### Models
- ML Models: `backend/model_cache/`
- Database Schema: `backend/app/models/`

### Logs
- Backend logs: Console output
- Audit logs: Database `audit_logs` table

## Environment Variables

```bash
# Backend .env file
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key
ML_MODEL_CACHE_DIR=./model_cache
LOG_LEVEL=INFO
MODERATION_LATENCY_THRESHOLD_MS=100
```

## Performance Benchmarks

| Metric | Target | Typical |
|--------|--------|---------|
| Moderation Latency | <100ms | 50-70ms |
| Throughput | >50 req/s | 75-100 req/s |
| Database Query | <10ms | 5-10ms |
| ML Inference | <50ms | 20-40ms |

## Monitoring Checklist

- [ ] Average latency < 100ms
- [ ] Flag rate reasonable (2-10%)
- [ ] Block rate acceptable (1-5%)
- [ ] No errors in logs
- [ ] Database responsive
- [ ] All rules active as expected

## Development Workflow

1. **Add New Feature**
   - Update backend code
   - Create/update API endpoint
   - Update frontend component
   - Test manually
   - Run automated tests

2. **Add New Rule**
   - Use Admin Panel or API
   - Test with sample messages
   - Monitor audit logs
   - Adjust threshold if needed

3. **Debug Issue**
   - Check backend logs
   - Review audit logs
   - Test API directly
   - Check database state

## Production Checklist

- [ ] Change SECRET_KEY
- [ ] Use production database
- [ ] Enable HTTPS
- [ ] Add authentication
- [ ] Configure CORS properly
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Load testing
- [ ] Security audit
- [ ] Documentation updated

## Useful Python Scripts

### Run Tests
```bash
cd backend
python test_api.py
```

### Initialize Database
```bash
cd backend
python init_db.py
```

### Check System Health
```python
import requests
r = requests.get('http://localhost:8000/health')
print(r.json())
```

## Docker Commands

### Start with Docker
```bash
docker-compose up
```

### Stop Services
```bash
docker-compose down
```

### Rebuild
```bash
docker-compose up --build
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Keyboard Shortcuts (Frontend)

- **Send Message**: Enter
- **New Line**: Shift + Enter
- **Switch to Admin**: Click "Admin Panel"
- **Refresh Stats**: Refresh page or re-open tab

## API Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |

## Default Credentials

**Database (Development):**
- User: `postgres`
- Password: `postgres`
- Database: `moderation_db`

⚠️ **Change in production!**

## Support Resources

- **Documentation**: See README.md, SETUP.md, ARCHITECTURE.md
- **API Docs**: http://localhost:8000/docs
- **Testing Guide**: TESTING.md
- **System Flow**: SYSTEM_FLOW.md

## Version Information

- Python: 3.9+
- Node.js: 16+
- PostgreSQL: 13+
- FastAPI: 0.104+
- React: 18+

## Quick Troubleshooting

**Problem:** Can't access frontend
```bash
# Check if running
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows
```

**Problem:** Can't access backend
```bash
# Check if running
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

**Problem:** Database not accessible
```bash
# Test connection
psql -U postgres -d moderation_db -c "SELECT 1;"
```

## Tips & Best Practices

1. **Always test in dev first** before updating production rules
2. **Monitor latency** regularly via Admin Panel
3. **Review audit logs** periodically for false positives
4. **Keep thresholds tuned** based on your use case
5. **Use session_id** for tracking user conversations
6. **Back up database** regularly
7. **Update dependencies** periodically for security

## Next Steps After Setup

1. ✅ Test basic chat functionality
2. ✅ Try different regions
3. ✅ Review audit logs
4. ✅ Check statistics
5. ✅ Create custom rule
6. ✅ Test rule update (zero downtime)
7. ✅ Run performance tests
8. ✅ Integrate with your chatbot/LLM

---

**Need Help?**
- Check documentation in project root
- Review API docs at /docs endpoint
- Examine audit logs for debugging
- Test APIs with curl or Postman
