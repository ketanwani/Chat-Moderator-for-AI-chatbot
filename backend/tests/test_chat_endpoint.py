"""
Integration tests for Chat Endpoint

Essential tests covering:
- Successful chat requests
- Content moderation integration
- Error handling
- Failsafe mechanisms
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.db.base import Base, get_db
from app.models.moderation_rule import Region


# Test Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client"""
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


class TestChatEndpoint:
    """Essential integration tests for chat endpoint"""

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

    @patch('app.api.chat.chatbot_service')
    @patch('app.api.chat.moderation_service')
    def test_chat_moderated_response(self, mock_moderation, mock_chatbot, client):
        """Test chat with content that gets moderated"""
        from app.schemas.moderation import ModerationResult

        mock_chatbot.generate_response.return_value = "You're an idiot!"
        mock_moderation.moderate_response.return_value = ModerationResult(
            is_flagged=True,
            is_blocked=True,
            final_response="I'm sorry, but I can't provide that response.",
            flagged_rules=[{"rule_type": "toxicity", "rule_id": 1}],
            scores={"toxicity": 0.95},
            latency_ms=25.0
        )

        response = client.post(
            "/api/v1/chat",
            json={"message": "Say something mean", "region": "us"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["is_moderated"] is True

    @patch('app.api.chat.chatbot_service')
    @patch('app.api.chat.moderation_service')
    def test_chat_pii_blocked(self, mock_moderation, mock_chatbot, client):
        """Test that PII content is blocked"""
        from app.schemas.moderation import ModerationResult

        mock_chatbot.generate_response.return_value = "My email is bot@example.com"
        mock_moderation.moderate_response.return_value = ModerationResult(
            is_flagged=True,
            is_blocked=True,
            final_response="I cannot share personal information.",
            flagged_rules=[{"rule_type": "pii", "rule_id": 2}],
            scores={},
            latency_ms=20.0
        )

        response = client.post(
            "/api/v1/chat",
            json={"message": "What's your email?", "region": "us"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["is_moderated"] is True

    def test_chat_missing_message(self, client):
        """Test error handling for missing message"""
        response = client.post(
            "/api/v1/chat",
            json={"region": "us"}
        )

        assert response.status_code == 422

    @patch('app.api.chat.chatbot_service')
    @patch('app.api.chat.moderation_service')
    def test_chat_moderation_error_failsafe(self, mock_moderation, mock_chatbot, client):
        """Test failsafe when moderation service fails"""
        mock_chatbot.generate_response.return_value = "Some response"
        mock_moderation.moderate_response.side_effect = Exception("Moderation error")

        response = client.post(
            "/api/v1/chat",
            json={"message": "Test", "region": "us"}
        )

        assert response.status_code == 200
        data = response.json()
        # Should return safe fallback message
        assert "temporarily unable" in data["response"].lower() or "error" in data["response"].lower()

    @patch('app.api.chat.chatbot_service')
    @patch('app.api.chat.moderation_service')
    def test_chat_with_session_id(self, mock_moderation, mock_chatbot, client):
        """Test chat with session tracking"""
        from app.schemas.moderation import ModerationResult

        mock_chatbot.generate_response.return_value = "Test response"
        mock_moderation.moderate_response.return_value = ModerationResult(
            is_flagged=False,
            is_blocked=False,
            final_response="Test response",
            flagged_rules=[],
            scores={},
            latency_ms=10.0
        )

        response = client.post(
            "/api/v1/chat",
            json={"message": "Test", "region": "us", "session_id": "test-123"}
        )

        assert response.status_code == 200
        mock_chatbot.generate_response.assert_called_once()

    @patch('app.api.chat.chatbot_service')
    @patch('app.api.chat.moderation_service')
    def test_chat_latency_tracking(self, mock_moderation, mock_chatbot, client):
        """Test that latency is tracked"""
        from app.schemas.moderation import ModerationResult

        mock_chatbot.generate_response.return_value = "Quick response"
        mock_moderation.moderate_response.return_value = ModerationResult(
            is_flagged=False,
            is_blocked=False,
            final_response="Quick response",
            flagged_rules=[],
            scores={},
            latency_ms=5.5
        )

        response = client.post(
            "/api/v1/chat",
            json={"message": "Fast test", "region": "us"}
        )

        assert response.status_code == 200
        # Latency should be tracked in moderation result
        mock_moderation.moderate_response.assert_called_once()
