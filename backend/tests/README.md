# Test Suite

Comprehensive unit and integration tests for the Moderation Engine.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## Test Files

| File | Tests | Coverage | Description |
|------|-------|----------|-------------|
| `test_ml_detector.py` | 40+ | PII, Toxicity, Financial, Medical detection |
| `test_moderation_service.py` | 30+ | Rule application, moderation flow, SLA |
| `test_chatbot_service.py` | 25+ | LLM providers, mock responses, fallbacks |
| `test_chat_endpoint.py` | 15+ | API integration, metrics, E2E workflows |

**Total: 100+ tests**

## Test Categories

### Unit Tests
- Individual component testing
- Fast execution
- Mocked dependencies
- 70+ tests

### Integration Tests
- Multiple components
- Database interactions
- Service integration
- 20+ tests

### E2E Tests
- Complete workflows
- API endpoints
- Real scenarios
- 10+ tests

## Running Tests

### All Tests
```bash
pytest
```

### Specific File
```bash
pytest tests/test_ml_detector.py
pytest tests/test_moderation_service.py
pytest tests/test_chatbot_service.py
pytest tests/test_chat_endpoint.py
```

### By Category
```bash
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m e2e            # End-to-end tests only
```

### By Pattern
```bash
pytest -k "pii"          # All PII-related tests
pytest -k "toxic"        # All toxicity tests
pytest -k "medical"      # All medical tests
```

## Coverage

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Open report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

**Target Coverage: 70%+**

## What's Tested

### ML Detector ✅
- ✅ PII detection (email, phone, SSN, credit card, IP)
- ✅ Toxicity detection with thresholds
- ✅ Financial terms detection
- ✅ Medical terms detection
- ✅ Keyword and regex matching
- ✅ Error handling
- ✅ Edge cases

### Moderation Service ✅
- ✅ Rule application logic
- ✅ Response blocking/allowing
- ✅ Fallback messages
- ✅ SLA latency tracking
- ✅ Audit logging
- ✅ Multiple rules handling
- ✅ Error recovery

### Chatbot Service ✅
- ✅ Provider initialization (OpenAI, Anthropic, Ollama, Mock)
- ✅ Mock responses for testing
- ✅ Fallback responses
- ✅ Error handling
- ✅ Conversation history
- ✅ Different LLM providers

### Chat Endpoint ✅
- ✅ Request/response handling
- ✅ Moderation integration
- ✅ Metrics collection
- ✅ Error handling
- ✅ Failsafe mechanisms
- ✅ E2E workflows

## CI/CD Ready

Tests are configured for:
- GitHub Actions
- GitLab CI
- Jenkins
- Travis CI

See `../TESTING.md` for CI/CD examples.

## Documentation

Full documentation: [../TESTING.md](../TESTING.md)

## Quick Reference

```bash
# Run tests
pytest

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show coverage
pytest --cov=app

# Run specific test
pytest tests/test_ml_detector.py::TestMLDetector::test_detect_pii_email
```

---

**Happy Testing!** 🧪
