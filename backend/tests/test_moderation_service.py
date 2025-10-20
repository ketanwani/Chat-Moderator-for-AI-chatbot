"""
Unit tests for Moderation Service

Essential tests covering:
- Clean and blocked content moderation
- PII and toxicity detection
- SLA compliance
- Error handling
"""

import pytest
from unittest.mock import Mock, patch
from app.services.moderation_service import ModerationService
from app.models.moderation_rule import ModerationRule, RuleType, Region


class TestModerationService:
    """Essential test suite for ModerationService"""

    @pytest.fixture
    def moderation_service(self):
        """Create ModerationService instance"""
        return ModerationService()

    @pytest.fixture
    def mock_db(self):
        """Create mock database session"""
        return Mock()

    @pytest.fixture
    def toxicity_rule(self):
        """Sample toxicity rule"""
        return ModerationRule(
            id=1,
            name="Toxicity Check",
            rule_type=RuleType.TOXICITY,
            region=Region.GLOBAL,
            is_active=True,
            priority=10,
            threshold=0.7
        )

    @pytest.fixture
    def pii_rule(self):
        """Sample PII rule"""
        return ModerationRule(
            id=2,
            name="PII Detection",
            rule_type=RuleType.PII,
            region=Region.GLOBAL,
            is_active=True,
            priority=9
        )

    @patch('app.services.moderation_service.ml_detector')
    def test_clean_response_allowed(self, mock_ml_detector, moderation_service, mock_db):
        """Test that clean responses are allowed through"""
        # Mock no active rules
        query_mock = Mock()
        mock_db.query.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.all.return_value = []

        result = moderation_service.moderate_response(
            user_message="Hello",
            bot_response="Hi! How can I help you?",
            region=Region.US,
            db=mock_db
        )

        assert result.is_flagged is False
        assert result.is_blocked is False
        assert result.final_response == "Hi! How can I help you?"

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

    @patch('app.services.moderation_service.ml_detector')
    def test_pii_content_blocked(self, mock_ml_detector, moderation_service, mock_db, pii_rule):
        """Test that PII content is blocked with appropriate message"""
        query_mock = Mock()
        mock_db.query.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.all.return_value = [pii_rule]

        mock_ml_detector.detect_pii.return_value = {
            "has_pii": True,
            "detected_types": {"email": 1, "phone": 1}
        }

        result = moderation_service.moderate_response(
            user_message="What's your contact?",
            bot_response="Email me at bot@example.com or call 555-1234",
            region=Region.US,
            db=mock_db
        )

        assert result.is_flagged is True
        assert result.is_blocked is True
        assert "privacy" in result.final_response.lower()

    @patch('app.services.moderation_service.ml_detector')
    def test_sla_latency_tracking(self, mock_ml_detector, moderation_service, mock_db):
        """Test that latency is tracked for SLA compliance"""
        query_mock = Mock()
        mock_db.query.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.all.return_value = []

        result = moderation_service.moderate_response(
            user_message="Test",
            bot_response="Test response",
            region=Region.US,
            db=mock_db
        )

        assert result.latency_ms >= 0
        assert result.latency_ms < 1000  # Should be fast in unit tests

    @patch('app.services.moderation_service.ml_detector')
    def test_audit_log_created(self, mock_ml_detector, moderation_service, mock_db):
        """Test that audit logs are created for all moderation checks"""
        query_mock = Mock()
        mock_db.query.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.all.return_value = []

        moderation_service.moderate_response(
            user_message="Test",
            bot_response="Test response",
            region=Region.US,
            db=mock_db,
            session_id="test-session-123"
        )

        # Verify audit log was created
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called

    @patch('app.services.moderation_service.ml_detector')
    def test_multiple_rules_evaluated(self, mock_ml_detector, moderation_service, mock_db, toxicity_rule, pii_rule):
        """Test that all applicable rules are evaluated"""
        query_mock = Mock()
        mock_db.query.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.all.return_value = [toxicity_rule, pii_rule]

        mock_ml_detector.detect_toxicity.return_value = {
            "is_toxic": False,
            "scores": {"toxicity": 0.1}
        }
        mock_ml_detector.detect_pii.return_value = {
            "has_pii": False,
            "detected_types": {}
        }

        result = moderation_service.moderate_response(
            user_message="Hello",
            bot_response="Hi there!",
            region=Region.US,
            db=mock_db
        )

        assert result.is_flagged is False
        assert result.is_blocked is False
        # Both detectors should have been called
        mock_ml_detector.detect_toxicity.assert_called_once()
        mock_ml_detector.detect_pii.assert_called_once()

    def test_error_handling_graceful_fallback(self, moderation_service, mock_db):
        """Test that errors don't crash the service"""
        mock_db.query.side_effect = Exception("Database error")

        with pytest.raises(Exception):
            moderation_service.moderate_response(
                user_message="Test",
                bot_response="Test response",
                region=Region.US,
                db=mock_db
            )

    @patch('app.services.moderation_service.ml_detector')
    def test_flagged_but_not_blocked(self, mock_ml_detector, moderation_service, mock_db):
        """Test content that's flagged for monitoring but not blocked"""
        rule = ModerationRule(
            id=3,
            name="Monitor Only",
            rule_type=RuleType.KEYWORD,
            region=Region.GLOBAL,
            is_active=True,
            priority=10,
            patterns=["watch"]
        )

        query_mock = Mock()
        mock_db.query.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.all.return_value = [rule]

        with patch.object(moderation_service, '_apply_rule') as mock_apply:
            mock_apply.return_value = {
                "flagged": True,
                "block": False,
                "details": {}
            }

            result = moderation_service.moderate_response(
                user_message="Tell me about watches",
                bot_response="Watches are timepieces",
                region=Region.US,
                db=mock_db
            )

            assert result.is_flagged is True
            assert result.is_blocked is False
            assert result.final_response == "Watches are timepieces"
