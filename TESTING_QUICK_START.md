# Testing Quick Start Guide

> **🚀 No Python installation needed - everything runs in Docker!**

## Prerequisites

1. **Docker Desktop** must be installed and running
2. **Containers must be started**

```bash
# Start containers (if not already running)
docker-compose up -d

# Verify backend container is running
docker ps | grep moderation_backend
```

---

## Run Tests (Choose One Method)

### Method 1: Use Helper Scripts (Easiest)

**Windows:**
```bash
run_tests.bat
```

**Linux/Mac:**
```bash
chmod +x run_tests.sh  # First time only
./run_tests.sh
```

### Method 2: Direct Docker Command

```bash
# Run all tests with output
docker exec moderation_backend python -m pytest tests/ -v

# Quick run (less output)
docker exec moderation_backend python -m pytest tests/ -q
```

---

## Common Test Commands

```bash
# Run all tests (35 tests)
docker exec moderation_backend python -m pytest tests/ -v

# Run specific test file
docker exec moderation_backend python -m pytest tests/test_moderation_service.py -v
docker exec moderation_backend python -m pytest tests/test_ml_detector.py -v
docker exec moderation_backend python -m pytest tests/test_chatbot_service.py -v
docker exec moderation_backend python -m pytest tests/test_chat_endpoint.py -v

# Run tests matching a keyword
docker exec moderation_backend python -m pytest tests/ -k "pii" -v
docker exec moderation_backend python -m pytest tests/ -k "toxic" -v

# Stop on first failure
docker exec moderation_backend python -m pytest tests/ -x

# Show coverage report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=term-missing

# Generate HTML coverage report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=html
```

---

## Test Status

```
✅ Total Tests: 35
✅ Passing: 35 (100%)
✅ Code Coverage: 66%
✅ Average Duration: <1 second
```

**Test Breakdown:**
- **test_moderation_service.py**: 8 tests (Core moderation logic)
- **test_ml_detector.py**: 12 tests (PII, toxicity, financial/medical detection)
- **test_chatbot_service.py**: 8 tests (Mock provider, responses, fallbacks)
- **test_chat_endpoint.py**: 7 tests (API integration, error handling)

---

## Troubleshooting

### Container Not Running

```bash
# Start containers
docker-compose up -d

# Check container status
docker ps
```

### Tests Failing

```bash
# Restart containers
docker-compose down
docker-compose up -d

# Check logs
docker logs moderation_backend
```

### Permission Issues (Linux/Mac)

```bash
# Make script executable
chmod +x run_tests.sh
```

---

## What's Being Tested?

### Core Functionality
- ✅ Content moderation (blocking toxic/harmful content)
- ✅ PII detection (emails, phones, SSN, credit cards)
- ✅ Toxicity scoring
- ✅ Financial & medical term detection
- ✅ SLA compliance (<100ms latency)
- ✅ Audit logging
- ✅ API endpoints
- ✅ Error handling & failsafes

### Key Success Metrics
- ✅ 100% response interception (failsafe mechanism)
- ✅ Sub-100ms moderation latency
- ✅ Accurate content detection
- ✅ Proper error handling

---

## Need More Details?

📖 **Full Documentation**: [backend/TESTING.md](backend/TESTING.md)

📚 **Main README**: [README.md](README.md)

🐛 **Report Issues**: Create an issue in the repository

---

## Quick Tips

💡 **Tip 1**: Use helper scripts (`run_tests.bat` / `run_tests.sh`) for the easiest experience

💡 **Tip 2**: Tests run fast (~10 seconds for all 35 tests)

💡 **Tip 3**: No need to install Python, pytest, or any packages locally

💡 **Tip 4**: Coverage reports are generated in `backend/htmlcov/` - open `index.html` in a browser

---

**Happy Testing!** 🧪✅
