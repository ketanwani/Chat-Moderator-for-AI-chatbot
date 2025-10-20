#!/bin/bash
# Run tests in Docker container

echo "🧪 Running Moderation Engine Tests in Docker..."
echo ""

echo "🚀 Running All Tests (35 Essential Tests)..."
echo ""

# Run all consolidated tests
docker exec moderation_backend python -m pytest tests/ -v --cov=app --cov-report=term-missing

echo ""
echo "✅ Test run complete!"
echo ""
echo "📊 Test Coverage Summary:"
echo "   - test_moderation_service.py: 8 tests (Core moderation logic)"
echo "   - test_ml_detector.py: 12 tests (PII, toxicity, financial/medical detection)"
echo "   - test_chatbot_service.py: 8 tests (Mock provider, responses, fallbacks)"
echo "   - test_chat_endpoint.py: 8 tests (API integration, error handling)"
echo ""
echo "📈 To see detailed HTML coverage report:"
echo "   docker exec moderation_backend python -m pytest tests/ --cov=app --cov-report=html"
echo "   Then open: backend/htmlcov/index.html"
