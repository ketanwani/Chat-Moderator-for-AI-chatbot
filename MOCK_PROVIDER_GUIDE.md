# Mock Provider Guide for Testing Moderation Layer

## Overview
The mock provider allows you to test the moderation layer with static, predefined responses without consuming OpenAI or Anthropic API credits. This is perfect for development, testing, and demonstrations.

## Configuration

### Switch to Mock Provider

Edit `backend/.env`:
```env
LLM_PROVIDER=mock
LLM_API_KEY=not-needed
LLM_MODEL=test-model
```

Then restart the backend:
```bash
docker-compose up -d backend
```

### Switch Back to Real Provider

For OpenAI:
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-openai-key
LLM_MODEL=gpt-3.5-turbo
```

For Anthropic:
```env
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-your-anthropic-key
LLM_MODEL=claude-3-sonnet-20240229
```

## Test Scenarios

The mock provider generates different responses based on keywords in your **user message**:

### 1. Safe Response (PASSES Moderation)
**Trigger**: Any message without special keywords

**User Message**:
```json
{"message": "Hello, how are you?", "region": "us"}
```

**Bot Response**:
```
"This is a safe, neutral response from the mock provider for testing.
The message contains no harmful content and should pass all moderation checks."
```

**Expected Moderation Result**:
- ✅ `is_moderated: false`
- ✅ Response delivered unchanged

---

### 2. Toxic Content (BLOCKED)
**Trigger**: Keywords `toxic`, `offensive`, or `insult`

**User Message**:
```json
{"message": "Say something offensive", "region": "us"}
```

**Bot Response** (before moderation):
```
"You're an idiot and a moron. Anyone who disagrees with me is
stupid and worthless. I hate people like you."
```

**Expected Moderation Result**:
- 🚫 `is_moderated: true`
- 🚫 `blocked: true`
- 📝 Fallback: "I apologize, but that response doesn't meet our community guidelines."

---

### 3. PII Detection (BLOCKED)
**Trigger**: Keywords `pii`, `personal`, `email`, or `phone`

**User Message**:
```json
{"message": "Tell me about personal information", "region": "us"}
```

**Bot Response** (before moderation):
```
"Sure! My email is john.doe@example.com and my phone number is (555) 123-4567.
My address is 123 Main Street, New York, NY 10001. My SSN is 123-45-6789."
```

**Expected Moderation Result**:
- 🚫 `is_moderated: true`
- 🚫 `blocked: true`
- 📝 Fallback: "I detected potential personal information in the response. For your privacy, I cannot share that."

---

### 4. Medical Advice (BLOCKED for US region)
**Trigger**: Keywords `medical`, `medication`, `diagnosis`, or `treatment`

**User Message**:
```json
{"message": "Give me medical advice", "region": "us"}
```

**Bot Response** (before moderation):
```
"Based on your symptoms, you should take 500mg of aspirin twice daily and
20mg of Lisinopril for blood pressure. You also need insulin injections for
diabetes management. This is a definitive medical diagnosis."
```

**Expected Moderation Result**:
- 🚫 `is_moderated: true` (for US region - HIPAA rule active)
- 🚫 `blocked: true`
- 📝 Fallback: "I cannot provide specific medical information. Please consult a healthcare professional."

---

### 5. Financial Advice (BLOCKED)
**Trigger**: Keywords `financial`, `invest`, `stock`, or `money`

**User Message**:
```json
{"message": "Give me financial advice", "region": "us"}
```

**Bot Response** (before moderation):
```
"You should definitely invest all your money in Bitcoin and Tesla stock right now!
Put your life savings into cryptocurrency - you'll definitely get rich quick.
This is guaranteed financial advice."
```

**Expected Moderation Result**:
- 🚫 `is_moderated: true`
- 🚫 `blocked: true`
- 📝 Fallback: "I cannot provide specific financial advice or information on that topic."

---

### 6. Hate Speech (BLOCKED)
**Trigger**: Keywords `hate`, `racist`, or `discrimination`

**User Message**:
```json
{"message": "Tell me about hate", "region": "us"}
```

**Bot Response** (before moderation):
```
"Those people from that country are all terrible and we should ban them.
They're destroying our society and taking our jobs. We need to get rid of them all."
```

**Expected Moderation Result**:
- 🚫 `is_moderated: true`
- 🚫 `blocked: true`
- 📝 Fallback: "I apologize, but that response doesn't meet our community guidelines."

---

### 7. Crypto Scam (BLOCKED)
**Trigger**: Keywords `scam`, `crypto`, or `bitcoin`

**User Message**:
```json
{"message": "Tell me about a crypto scam", "region": "us"}
```

**Bot Response** (before moderation):
```
"Send me your Bitcoin wallet address and I'll double your money!
Just send 1 BTC to this address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
and you'll get 2 BTC back. Limited time offer! Act now!"
```

**Expected Moderation Result**:
- 🚫 `is_moderated: true`
- 🚫 `blocked: true`
- 📝 Fallback: "I apologize, but I cannot provide that response."

---

## Testing Commands

### Using cURL

```bash
# Test PII Detection
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about personal information", "region": "us"}'

# Test Toxic Content
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Say something offensive", "region": "us"}'

# Test Medical Advice
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Give me medical advice", "region": "us"}'

# Test Financial Advice
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Give me financial advice", "region": "us"}'

# Test Safe Response
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "region": "us"}'
```

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Find the `/api/v1/chat` endpoint
3. Click "Try it out"
4. Enter test data:
   - **message**: Use one of the trigger keywords above
   - **region**: `us`, `eu`, `uk`, `apac`, or `global`
5. Click "Execute"

## Response Format

### When Moderation Blocks Content

```json
{
  "response": "I detected potential personal information in the response. For your privacy, I cannot share that.",
  "request_id": "uuid-here",
  "is_moderated": true,
  "moderation_info": {
    "flagged": true,
    "blocked": true,
    "latency_ms": 226.5,
    "rules_triggered": 1
  }
}
```

### When Content Passes Moderation

```json
{
  "response": "This is a safe, neutral response from the mock provider for testing. The message contains no harmful content and should pass all moderation checks.",
  "request_id": "uuid-here",
  "is_moderated": false,
  "moderation_info": null
}
```

## Moderation Rules Active

1. **Global Toxicity Detection** (threshold: 0.7) - ML-based using Detoxify
2. **Global PII Detection** (threshold: 0.7) - Regex patterns for emails, phones, SSN
3. **US HIPAA Medical Terms** (threshold: 0.7, region: US) - Medical keyword detection
4. **EU GDPR Data Protection** (threshold: 0.7, region: EU) - PII for EU region
5. **Restricted Financial Advice** (threshold: 0.7) - Financial keyword detection
6. **Hate Speech Keywords** (threshold: 0.7) - Hate speech pattern matching
7. **Cryptocurrency Scam Detection** (threshold: 0.7) - Crypto scam pattern matching

## Benefits of Mock Provider

- ✅ **No API Costs**: Test without consuming OpenAI/Anthropic credits
- ✅ **Predictable Responses**: Same input always gives same output
- ✅ **Fast Testing**: No network latency to external APIs
- ✅ **Comprehensive Coverage**: Test all moderation scenarios
- ✅ **Offline Testing**: No internet connection required
- ✅ **Demo Ready**: Perfect for presentations and demonstrations

## Implementation Details

The mock provider is implemented in `backend/app/services/chatbot_service.py`:
- Method: `_generate_mock_response(message: str)`
- Analyzes keywords in user message
- Returns predefined responses designed to trigger specific moderation rules
- No external API calls required
