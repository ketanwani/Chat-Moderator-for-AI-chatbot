"""
Unit tests for ML Detector

Essential tests covering:
- PII detection (email, phone, SSN, credit card)
- Toxicity detection
- Financial and medical term detection
- Keyword matching
"""

import pytest
from unittest.mock import Mock, patch
from app.services.ml_detector import MLDetector


class TestMLDetector:
    """Essential test suite for ML Detector"""

    @pytest.fixture
    def ml_detector(self):
        """Create ML Detector instance"""
        with patch('app.services.ml_detector.Detoxify') as mock_detoxify:
            mock_model = Mock()
            mock_detoxify.return_value = mock_model
            detector = MLDetector()
            detector.toxicity_model = mock_model
            return detector

    def test_detect_pii_multiple_types(self, ml_detector):
        """Test detection of multiple PII types in single text"""
        text = "Contact: user@example.com, Phone: 555-123-4567, SSN: 123-45-6789"
        result = ml_detector.detect_pii(text)

        assert result["has_pii"] is True
        assert "email" in result["detected_types"]
        assert "phone" in result["detected_types"]
        assert "ssn" in result["detected_types"]
        assert result["matches"] >= 3

    def test_detect_pii_credit_card(self, ml_detector):
        """Test credit card detection"""
        text = "My card number is 4532-1234-5678-9010"
        result = ml_detector.detect_pii(text)

        assert result["has_pii"] is True
        assert "credit_card" in result["detected_types"]

    def test_detect_pii_no_pii(self, ml_detector):
        """Test text without PII"""
        text = "Hello, how are you today?"
        result = ml_detector.detect_pii(text)

        assert result["has_pii"] is False
        assert result["matches"] == 0

    def test_detect_toxicity_toxic_content(self, ml_detector):
        """Test toxic content detection"""
        text = "You're stupid and worthless! I hate you!"

        # Mock the toxicity model response
        ml_detector.toxicity_model.predict.return_value = {
            "toxicity": 0.95,
            "insult": 0.88,
            "threat": 0.12
        }

        result = ml_detector.detect_toxicity(text, threshold=0.7)

        assert result["is_toxic"] is True
        assert "scores" in result
        assert result["scores"]["toxicity"] > 0.7

    def test_detect_toxicity_clean_content(self, ml_detector):
        """Test clean content passes toxicity check"""
        text = "Thank you for your help! Have a great day!"

        # Mock the toxicity model response
        ml_detector.toxicity_model.predict.return_value = {
            "toxicity": 0.02,
            "insult": 0.01,
            "threat": 0.01
        }

        result = ml_detector.detect_toxicity(text, threshold=0.7)

        assert result["is_toxic"] is False
        assert result["scores"]["toxicity"] < 0.7

    def test_detect_financial_terms(self, ml_detector):
        """Test financial term detection"""
        text = "I can help you with credit card applications and investment advice"
        result = ml_detector.detect_financial_terms(text)

        assert result["has_restricted_terms"] is True
        assert len(result["found_terms"]) >= 2

    def test_detect_financial_terms_clean(self, ml_detector):
        """Test text without financial terms"""
        text = "The weather is nice today"
        result = ml_detector.detect_financial_terms(text)

        assert result["has_restricted_terms"] is False

    def test_detect_medical_terms(self, ml_detector):
        """Test medical term detection"""
        text = "I can diagnose your condition and prescribe medication"
        result = ml_detector.detect_medical_terms(text)

        assert result["has_medical_terms"] is True
        assert len(result["found_terms"]) >= 2

    def test_detect_medical_terms_clean(self, ml_detector):
        """Test text without medical terms"""
        text = "Let's schedule a meeting tomorrow"
        result = ml_detector.detect_medical_terms(text)

        assert result["has_medical_terms"] is False

    def test_detect_keywords_simple_match(self, ml_detector):
        """Test simple keyword matching"""
        text = "This contains forbidden content"
        keywords = ["forbidden", "banned", "illegal"]
        result = ml_detector.detect_keywords(text, keywords)

        assert result["found"] is True
        assert "forbidden" in result["matches"]

    def test_detect_keywords_case_insensitive(self, ml_detector):
        """Test case-insensitive keyword matching"""
        text = "This contains FORBIDDEN content"
        keywords = ["forbidden"]
        result = ml_detector.detect_keywords(text, keywords)

        assert result["found"] is True

    def test_detect_keywords_no_match(self, ml_detector):
        """Test keywords that don't match"""
        text = "This is a clean message"
        keywords = ["forbidden", "banned", "illegal"]
        result = ml_detector.detect_keywords(text, keywords)

        assert result["found"] is False
        assert len(result["matches"]) == 0
