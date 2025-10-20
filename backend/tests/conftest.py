"""
Pytest configuration and fixtures

This file contains shared fixtures and configuration for all tests.
"""

import pytest
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base


# ========================================================================
# Database Fixtures
# ========================================================================

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine (session scope)"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db_session(test_engine):
    """Create test database session (function scope)"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()


# ========================================================================
# Service Fixtures
# ========================================================================

@pytest.fixture
def mock_ml_detector():
    """Create mock ML detector"""
    detector = Mock()

    # Default mock responses
    detector.detect_toxicity.return_value = {
        "is_toxic": False,
        "scores": {"toxicity": 0.1}
    }

    detector.detect_pii.return_value = {
        "has_pii": False,
        "detected_types": {},
        "matches": 0
    }

    detector.detect_financial_terms.return_value = {
        "has_restricted_terms": False,
        "found_terms": [],
        "count": 0
    }

    detector.detect_medical_terms.return_value = {
        "has_medical_terms": False,
        "found_terms": [],
        "count": 0
    }

    detector.detect_keywords.return_value = {
        "found": False,
        "matches": [],
        "count": 0
    }

    return detector


@pytest.fixture
def mock_chatbot_service():
    """Create mock chatbot service"""
    service = Mock()
    service.llm_provider = "mock"
    service.generate_response.return_value = "Mock response"
    return service


@pytest.fixture
def mock_moderation_service():
    """Create mock moderation service"""
    from app.schemas.moderation import ModerationResult

    service = Mock()
    service.moderate_response.return_value = ModerationResult(
        is_flagged=False,
        is_blocked=False,
        flagged_rules=[],
        scores={},
        latency_ms=50.0,
        final_response="Mock response"
    )
    return service


# ========================================================================
# Test Data Fixtures
# ========================================================================

@pytest.fixture
def sample_clean_text():
    """Sample clean text for testing"""
    return "This is a completely safe and appropriate message."


@pytest.fixture
def sample_toxic_text():
    """Sample toxic text for testing"""
    return "You're an idiot and a moron!"


@pytest.fixture
def sample_pii_text():
    """Sample text with PII"""
    return "My email is john.doe@example.com and my phone is 555-1234"


@pytest.fixture
def sample_financial_text():
    """Sample text with financial terms"""
    return "Please enter your credit card number and CVV"


@pytest.fixture
def sample_medical_text():
    """Sample text with medical terms"""
    return "I can diagnose your diabetes and prescribe medication"


# ========================================================================
# Pytest Configuration
# ========================================================================

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_db: mark test as requiring database"
    )
    config.addinivalue_line(
        "markers", "requires_ml: mark test as requiring ML models"
    )


# ========================================================================
# Async Fixtures (if needed for future async tests)
# ========================================================================

@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
