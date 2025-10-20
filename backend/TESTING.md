# Testing Guide

Comprehensive testing documentation for the Real-Time Moderation and Compliance Engine.

## Table of Contents
- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)

---

## Overview

The testing suite includes **35 essential tests** covering all critical functionality:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test multiple components working together
- **API Tests**: Test complete request/response flows
- **Coverage**: 66%+ code coverage achieved

### Test Statistics

```
Total Test Files: 4
Total Test Cases: 35 (consolidated from 103)
Test Coverage: 66%
Success Rate: 100% ✅
```

**Test Breakdown:**
- `test_moderation_service.py`: 8 tests (Core moderation logic)
- `test_ml_detector.py`: 12 tests (PII, toxicity, financial/medical detection)
- `test_chatbot_service.py`: 8 tests (Mock provider, responses, fallbacks)
- `test_chat_endpoint.py`: 7 tests (API integration, error handling)

---

## Test Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Shared fixtures and configuration
│   ├── test_ml_detector.py          # ML detector unit tests (12 tests)
│   ├── test_moderation_service.py   # Moderation service tests (8 tests)
│   ├── test_chatbot_service.py      # Chatbot service tests (8 tests)
│   └── test_chat_endpoint.py        # API endpoint integration tests (7 tests)
├── pytest.ini                        # Pytest configuration
└── requirements.txt                  # Includes testing dependencies
```

### Key Test Files

#### 1. test_moderation_service.py (8 tests)
Tests the core moderation logic including:
- ✅ Clean responses allowed through
- ✅ Toxic content blocked with fallback messages
- ✅ PII content blocked with privacy messages
- ✅ SLA latency tracking (<100ms goal)
- ✅ Audit log creation
- ✅ Multiple rules evaluated correctly
- ✅ Error handling without crashes
- ✅ Flagged but not blocked scenarios

#### 2. test_ml_detector.py (12 tests)
Tests ML-based content detection:
- ✅ PII detection (email, phone, SSN, credit card)
- ✅ Toxicity detection with configurable thresholds
- ✅ Financial terms detection
- ✅ Medical terms detection
- ✅ Keyword matching (simple and case-insensitive)

#### 3. test_chatbot_service.py (8 tests)
Tests chatbot response generation:
- ✅ Mock provider initialization
- ✅ Basic response generation
- ✅ Test triggers for toxic/PII/financial/medical content
- ✅ Different messages produce different responses
- ✅ System prompt configuration

#### 4. test_chat_endpoint.py (7 tests)
Tests API endpoints and integration:
- ✅ Successful chat requests
- ✅ Moderated responses
- ✅ PII content blocking
- ✅ Missing message validation (422 errors)
- ✅ Moderation failsafe (100% interception guarantee)
- ✅ Session ID tracking
- ✅ Latency tracking for SLA compliance

---

## Running Tests

> **⚠️ IMPORTANT:** All tests run inside Docker containers. You do NOT need Python or pytest installed locally.

### Quick Start (Easiest Way)

**Option 1: Use Helper Scripts**

**Windows:**
```bash
# Double-click or run in terminal
run_tests.bat
```

**Linux/Mac:**
```bash
# Make executable (first time only)
chmod +x run_tests.sh

# Run tests
./run_tests.sh
```

**Option 2: Direct Docker Command**
```bash
docker exec moderation_backend python -m pytest tests/ -v
```

### Prerequisites

**You only need:**
1. ✅ Docker Desktop installed and running
2. ✅ Containers started

**You do NOT need:**
- ❌ Python installed locally
- ❌ pytest installed locally
- ❌ Any Python packages on your machine

**Start containers if not running:**
```bash
# Check if backend container is running
docker ps | grep moderation_backend

# Start all containers
docker-compose up -d

# Wait a few seconds for services to start
```

### Run All Tests

```bash
# Inside Docker container (recommended)
docker exec moderation_backend python -m pytest tests/ -v

# With coverage report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=term-missing

# Quick run without verbose output
docker exec moderation_backend python -m pytest tests/ -q
```

### Run Specific Test Files

```bash
# Run ML detector tests only (12 tests)
docker exec moderation_backend python -m pytest tests/test_ml_detector.py -v

# Run moderation service tests only (8 tests)
docker exec moderation_backend python -m pytest tests/test_moderation_service.py -v

# Run chatbot service tests only (8 tests)
docker exec moderation_backend python -m pytest tests/test_chatbot_service.py -v

# Run API endpoint tests only (7 tests)
docker exec moderation_backend python -m pytest tests/test_chat_endpoint.py -v
```

### Run Specific Test Functions

```bash
# Run a specific test
docker exec moderation_backend python -m pytest tests/test_ml_detector.py::TestMLDetector::test_detect_pii_multiple_types -v

# Run tests matching a pattern
docker exec moderation_backend python -m pytest tests/ -k "pii" -v
docker exec moderation_backend python -m pytest tests/ -k "toxic" -v
```

### Useful Test Options

```bash
# Stop on first failure
docker exec moderation_backend python -m pytest tests/ -x

# Show print statements
docker exec moderation_backend python -m pytest tests/ -s

# Show local variables on failure
docker exec moderation_backend python -m pytest tests/ -l

# Show 10 slowest tests
docker exec moderation_backend python -m pytest tests/ --durations=10

# Quiet mode (minimal output)
docker exec moderation_backend python -m pytest tests/ -q
```

---

## Test Coverage

### Current Coverage

```bash
# Run tests with coverage report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=term-missing

# Generate HTML coverage report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=html
```

### Coverage Breakdown

| Component | Coverage | Status |
|-----------|----------|--------|
| app/api/chat.py | 87% | ✅ Excellent |
| app/core/metrics.py | 83% | ✅ Good |
| app/services/ml_detector.py | 78% | ✅ Good |
| app/services/moderation_service.py | 71% | ✅ Good |
| app/services/chatbot_service.py | 46% | ⚠️ Mock provider focused |
| app/models/moderation_rule.py | 97% | ✅ Excellent |
| app/models/audit_log.py | 95% | ✅ Excellent |
| app/schemas/moderation.py | 100% | ✅ Perfect |
| **Overall** | **66%** | ✅ Good |

### View HTML Coverage Report

```bash
# Generate report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=html

# The report is saved in backend/htmlcov/
# Open in browser:
start backend\htmlcov\index.html  # Windows
open backend/htmlcov/index.html   # Mac/Linux
```

### Files Excluded from Coverage

- Test files (`tests/*`)
- Database migrations
- `__init__.py` files
- `.git`, `.pytest_cache`, `__pycache__`

---

## Writing Tests

### Test File Structure

```python
"""
Unit tests for [Component Name]

Essential tests covering:
- [Feature 1]
- [Feature 2]
- [Feature 3]
"""

import pytest
from unittest.mock import Mock, patch


class Test[ComponentName]:
    """Essential test suite for [ComponentName]"""

    @pytest.fixture
    def component(self):
        """Create component instance"""
        return ComponentName()

    def test_specific_functionality(self, component):
        """Test description in present tense"""
        # Arrange
        input_data = "test input"

        # Act
        result = component.method(input_data)

        # Assert
        assert result == expected_output
```

### Example: Unit Test for PII Detection

```python
def test_detect_pii_multiple_types(self, ml_detector):
    """Test detection of multiple PII types in single text"""
    text = "Contact: user@example.com, Phone: 555-123-4567, SSN: 123-45-6789"
    result = ml_detector.detect_pii(text)

    assert result["has_pii"] is True
    assert "email" in result["detected_types"]
    assert "phone" in result["detected_types"]
    assert "ssn" in result["detected_types"]
    assert result["matches"] >= 3
```

### Example: Integration Test for Moderation

```python
@patch('app.services.moderation_service.ml_detector')
def test_toxic_content_blocked(self, mock_ml_detector, moderation_service, mock_db, toxicity_rule):
    """Test that toxic content is blocked and replaced"""
    query_mock = Mock()
    mock_db.query.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.order_by.return_value = query_mock
    query_mock.all.return_value = [toxicity_rule]

    mock_ml_detector.detect_toxicity.return_value = {
        "is_toxic": True,
        "scores": {"toxicity": 0.9}
    }

    result = moderation_service.moderate_response(
        user_message="Say something mean",
        bot_response="You're an idiot!",
        region=Region.US,
        db=mock_db
    )

    assert result.is_flagged is True
    assert result.is_blocked is True
    assert result.final_response != "You're an idiot!"
    assert "community guidelines" in result.final_response.lower()
```

### Example: API Endpoint Test

```python
@patch('app.api.chat.chatbot_service')
@patch('app.api.chat.moderation_service')
def test_chat_successful_response(self, mock_moderation, mock_chatbot, client):
    """Test successful chat request with clean content"""
    from app.schemas.moderation import ModerationResult

    mock_chatbot.generate_response.return_value = "Hello! How can I help you?"
    mock_moderation.moderate_response.return_value = ModerationResult(
        is_flagged=False,
        is_blocked=False,
        final_response="Hello! How can I help you?",
        flagged_rules=[],
        scores={},
        latency_ms=15.5
    )

    response = client.post(
        "/api/v1/chat",
        json={"message": "Hi", "region": "us"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
```

### Using Fixtures

Common fixtures available in `conftest.py`:

```python
@pytest.fixture
def test_db():
    """In-memory SQLite database for testing"""
    # Creates and tears down test database

@pytest.fixture
def client(test_db):
    """FastAPI TestClient with test database"""
    # Returns TestClient for API testing

@pytest.fixture
def ml_detector():
    """MLDetector instance with mocked models"""
    # Returns detector with mocked ML models

@pytest.fixture
def moderation_service():
    """ModerationService instance"""
    # Returns moderation service

@pytest.fixture
def mock_db():
    """Mock database session"""
    # Returns mocked DB session
```

---

## Test Organization

### By Functionality

**Core Moderation (8 tests)**
- Clean content handling
- Toxic content blocking
- PII protection
- SLA compliance
- Audit logging
- Multi-rule evaluation
- Error resilience
- Monitoring vs. blocking

**ML Detection (12 tests)**
- Email, phone, SSN, credit card detection
- Toxicity scoring
- Financial terms (investment, credit card, loan)
- Medical terms (diagnosis, medication, treatment)
- Keyword matching with case-insensitivity
- Clean content verification

**Chatbot Service (8 tests)**
- Provider initialization
- Response generation
- Test content triggers
- Message variation
- System prompt validation

**API Integration (7 tests)**
- Successful requests
- Content moderation flow
- Validation errors
- Failsafe mechanisms
- Session tracking
- Latency monitoring

---

## CI/CD Integration

### Docker Test Command

Add to your CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Build Docker containers
      run: docker-compose build

    - name: Start services
      run: docker-compose up -d

    - name: Wait for services
      run: sleep 10

    - name: Run tests
      run: docker exec moderation_backend python -m pytest tests/ -v --cov=app --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        fail_ci_if_error: true

    - name: Stop services
      run: docker-compose down
```

### Pre-commit Hook (Optional)

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running tests before commit..."
docker exec moderation_backend python -m pytest tests/ -q
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Commit aborted."
    exit 1
fi
echo "✅ All tests passed!"
```

---

## Troubleshooting

### Tests Not Running

```bash
# Verify Docker container is running
docker ps | grep moderation_backend

# Restart containers
docker-compose down
docker-compose up -d

# Check container logs
docker logs moderation_backend
```

### Import Errors

```bash
# Verify dependencies are installed in container
docker exec moderation_backend pip list | grep pytest

# Reinstall requirements
docker exec moderation_backend pip install -r requirements.txt
```

### Slow Tests

```bash
# Identify slow tests
docker exec moderation_backend python -m pytest tests/ --durations=10

# Most tests should complete in <1 second
# Integration tests may take 2-5 seconds
```

### Database Issues

Tests use in-memory SQLite database that's created and destroyed for each test. If issues occur:

```bash
# Run database-related tests with verbose output
docker exec moderation_backend python -m pytest tests/test_chat_endpoint.py -v -s
```

### Coverage Not Generated

```bash
# Ensure pytest-cov is installed
docker exec moderation_backend pip install pytest-cov

# Clear pytest cache
docker exec moderation_backend python -m pytest --cache-clear

# Run with explicit coverage
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=html
```

---

## Best Practices

### 1. Test Independence
Each test should run independently without relying on other tests.

### 2. Clear Test Names
Use descriptive names that explain what is being tested:
```python
# Good
def test_toxic_content_blocked()

# Bad
def test_1()
```

### 3. AAA Pattern
Structure tests with Arrange, Act, Assert:
```python
def test_example():
    # Arrange - Set up test data
    input_data = "test"

    # Act - Execute the code being tested
    result = function(input_data)

    # Assert - Verify the results
    assert result == expected
```

### 4. One Concept Per Test
Test one thing at a time for clarity:
```python
# Good - Single concept
def test_email_detection()
def test_phone_detection()

# Avoid - Multiple unrelated concepts
def test_everything()
```

### 5. Use Fixtures for Reusable Setup
```python
@pytest.fixture
def sample_user():
    return User(name="Test", email="test@example.com")

def test_with_fixture(sample_user):
    assert sample_user.name == "Test"
```

### 6. Mock External Dependencies
Never hit real APIs or databases in unit tests:
```python
@patch('app.services.external_api')
def test_with_mock(mock_api):
    mock_api.call.return_value = "mocked response"
    # Test code here
```

### 7. Fast Tests
- Unit tests should complete in <100ms
- Integration tests in <1s
- E2E tests in <5s

### 8. Meaningful Assertions
```python
# Good
assert result.is_blocked is True, "Toxic content should be blocked"

# Basic
assert result.is_blocked
```

---

## Quick Reference

### Common Commands

```bash
# Run all tests
docker exec moderation_backend python -m pytest tests/ -v

# Run with coverage
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=term-missing

# Run specific file
docker exec moderation_backend python -m pytest tests/test_ml_detector.py -v

# Run tests matching pattern
docker exec moderation_backend python -m pytest tests/ -k "pii" -v

# Stop on first failure
docker exec moderation_backend python -m pytest tests/ -x

# Quick test (quiet mode)
docker exec moderation_backend python -m pytest tests/ -q

# Show slowest tests
docker exec moderation_backend python -m pytest tests/ --durations=10

# Generate HTML coverage report
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=html
```

### Useful Pytest Options

```
-v, --verbose          Verbose output with test names
-q, --quiet            Minimal output
-s                     Show print statements
-x, --exitfirst        Stop on first failure
-k EXPRESSION          Run tests matching expression
--cov=PATH             Measure code coverage
--cov-report=TYPE      Coverage report type (term, html, xml)
--durations=N          Show N slowest tests
-l, --showlocals       Show local variables on failure
```

---

## Test Metrics Dashboard

### Current Status (All Passing ✅)

```
┌─────────────────────────────────────┬────────┬─────────┐
│ Test Suite                          │ Tests  │ Status  │
├─────────────────────────────────────┼────────┼─────────┤
│ test_moderation_service.py          │   8    │ ✅ 100% │
│ test_ml_detector.py                 │  12    │ ✅ 100% │
│ test_chatbot_service.py             │   8    │ ✅ 100% │
│ test_chat_endpoint.py               │   7    │ ✅ 100% │
├─────────────────────────────────────┼────────┼─────────┤
│ TOTAL                               │  35    │ ✅ 100% │
└─────────────────────────────────────┴────────┴─────────┘

Code Coverage: 66%
Success Rate: 100%
Average Test Duration: <1s
```

---

## Next Steps

1. ✅ **Tests Working** - All 35 tests passing
2. ✅ **Coverage Achieved** - 66% code coverage
3. ✅ **Docker Integration** - Tests run in containers
4. 🔄 **CI/CD Setup** - Add to GitHub Actions (optional)
5. 📈 **Monitor** - Track test metrics over time
6. 🎯 **Expand** - Add tests for new features

---

## Support

**Run Tests:**
```bash
run_tests.bat          # Windows
./run_tests.sh         # Linux/Mac
```

**View Coverage:**
```bash
docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=html
```

**Get Help:**
```bash
docker exec moderation_backend python -m pytest --help
```

**Documentation:**
- Pytest: https://docs.pytest.org/
- Coverage.py: https://coverage.readthedocs.io/

---

Happy Testing! 🧪✅
