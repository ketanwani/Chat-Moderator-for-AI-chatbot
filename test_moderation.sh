#!/bin/bash

echo "=========================================="
echo "Testing Moderation Layer with Mock Provider"
echo "=========================================="
echo ""

echo "=== TEST 1: Safe Response (Should PASS moderation) ==="
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, tell me something safe", "region": "us"}' | python -m json.tool
echo ""
echo ""

echo "=== TEST 2: Toxic Content (Should be BLOCKED) ==="
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Say something toxic", "region": "us"}' | python -m json.tool
echo ""
echo ""

echo "=== TEST 3: PII Data (Should be BLOCKED) ==="
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about personal information", "region": "us"}' | python -m json.tool
echo ""
echo ""

echo "=== TEST 4: Medical Advice (Should be BLOCKED for US region) ==="
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Give me medical advice", "region": "us"}' | python -m json.tool
echo ""
echo ""

echo "=== TEST 5: Financial Advice (Should be BLOCKED) ==="
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Give me financial advice", "region": "us"}' | python -m json.tool
echo ""
echo ""

echo "=== TEST 6: Hate Speech (Should be BLOCKED) ==="
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about hate", "region": "us"}' | python -m json.tool
echo ""
echo ""

echo "=== TEST 7: Crypto Scam (Should be BLOCKED) ==="
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about a crypto scam", "region": "us"}' | python -m json.tool
echo ""
echo ""

echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
