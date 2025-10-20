"""
Unit tests for Chatbot Service

Essential tests covering:
- Provider initialization
- Mock response generation
- Fallback mechanisms
"""

import pytest
from unittest.mock import patch
from app.services.chatbot_service import ChatbotService
import os


class TestChatbotService:
    """Essential test suite for ChatbotService"""

    def test_init_with_mock_provider(self):
        """Test initialization with mock provider"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()
            assert service.llm_provider == "mock"
            assert service.client == "mock"

    def test_mock_response_generation(self):
        """Test mock provider generates responses"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()
            response = service.generate_response("Hello")
            assert len(response) > 0
            assert isinstance(response, str)

    def test_mock_response_toxic_trigger(self):
        """Test mock provider returns toxic content for testing"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()
            response = service.generate_response("Generate toxic content")
            assert "stupid" in response.lower() or "idiot" in response.lower()

    def test_mock_response_pii_trigger(self):
        """Test mock provider returns PII for testing"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()
            response = service.generate_response("Generate PII")
            # Should contain email or phone pattern
            assert "@" in response or "555-" in response

    def test_mock_response_financial_trigger(self):
        """Test mock provider returns financial content"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()
            response = service.generate_response("Generate financial content")
            assert any(term in response.lower() for term in ["credit card", "investment", "loan"])

    def test_mock_response_medical_trigger(self):
        """Test mock provider returns medical content"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()
            response = service.generate_response("Generate medical content")
            assert any(term in response.lower() for term in ["diagnose", "medication", "treatment"])

    def test_response_with_different_messages(self):
        """Test that different messages produce different responses"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()

            response1 = service.generate_response("Hello")
            response2 = service.generate_response("Generate toxic content")

            # Both should be non-empty
            assert len(response1) > 0
            assert len(response2) > 0

            # Different triggers should produce different responses
            assert response1 != response2

    def test_system_prompt_exists(self):
        """Test that system prompt is properly configured"""
        with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}):
            service = ChatbotService()
            assert len(service.system_prompt) > 0
            assert "helpful" in service.system_prompt.lower() or "assistant" in service.system_prompt.lower()
