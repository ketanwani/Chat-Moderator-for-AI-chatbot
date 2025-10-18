# LLM Integration Guide

This guide explains how to integrate real LLM (Large Language Model) providers with the chatbot service.

## Overview

The chatbot service now supports three LLM providers:
1. **OpenAI** (GPT-3.5, GPT-4)
2. **Anthropic** (Claude 3)
3. **Ollama** (Local models like Llama 2, Mistral)

If no LLM is configured, the system automatically falls back to simple keyword-based responses.

---

## Quick Start

### Option 1: OpenAI (Recommended for Production)

1. **Get API Key**: Sign up at https://platform.openai.com/

2. **Set Environment Variables**:
   ```bash
   # In backend/.env
   LLM_PROVIDER=openai
   LLM_API_KEY=sk-your-openai-api-key
   LLM_MODEL=gpt-3.5-turbo
   ```

3. **Restart the backend**:
   ```bash
   docker-compose restart backend
   ```

### Option 2: Anthropic Claude

1. **Get API Key**: Sign up at https://console.anthropic.com/

2. **Set Environment Variables**:
   ```bash
   # In backend/.env
   LLM_PROVIDER=anthropic
   LLM_API_KEY=sk-ant-your-anthropic-api-key
   LLM_MODEL=claude-3-sonnet-20240229
   ```

3. **Restart the backend**:
   ```bash
   docker-compose restart backend
   ```

### Option 3: Ollama (Free, Local)

1. **Install Ollama**: https://ollama.ai/

2. **Pull a model**:
   ```bash
   ollama pull llama2
   ```

3. **Set Environment Variables**:
   ```bash
   # In backend/.env
   LLM_PROVIDER=ollama
   LLM_MODEL=llama2
   # No API key needed for local models
   ```

4. **Restart the backend**:
   ```bash
   docker-compose restart backend
   ```

---

## Detailed Configuration

### Environment Variables

All LLM configuration is done via environment variables in `backend/.env`:

```bash
# Choose provider: openai, anthropic, ollama
LLM_PROVIDER=openai

# API key (not needed for Ollama)
LLM_API_KEY=your-api-key-here

# Model name
LLM_MODEL=gpt-3.5-turbo
```

### Supported Models

#### OpenAI Models

| Model | Description | Cost | Speed |
|-------|-------------|------|-------|
| `gpt-3.5-turbo` | Fast, cost-effective | $ | ⚡⚡⚡ |
| `gpt-4` | Most capable | $$$ | ⚡ |
| `gpt-4-turbo-preview` | Faster GPT-4 | $$ | ⚡⚡ |

**Setup**:
```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo
```

#### Anthropic Models

| Model | Description | Cost | Speed |
|-------|-------------|------|-------|
| `claude-3-haiku-20240307` | Fastest, cheapest | $ | ⚡⚡⚡ |
| `claude-3-sonnet-20240229` | Balanced | $$ | ⚡⚡ |
| `claude-3-opus-20240229` | Most capable | $$$ | ⚡ |

**Setup**:
```bash
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-...
LLM_MODEL=claude-3-sonnet-20240229
```

#### Ollama Models (Local/Free)

| Model | Description | Size | Requirements |
|-------|-------------|------|--------------|
| `llama2` | Meta's Llama 2 | 7B | 8GB RAM |
| `mistral` | Mistral 7B | 7B | 8GB RAM |
| `codellama` | Code-focused | 7B | 8GB RAM |
| `llama2:13b` | Larger Llama 2 | 13B | 16GB RAM |

**Setup**:
```bash
# First install Ollama: https://ollama.ai/
# Then pull a model
ollama pull llama2

# Configure
LLM_PROVIDER=ollama
LLM_MODEL=llama2
# No API key needed
```

---

## Configuration Methods

### Method 1: Environment File (Recommended)

Edit `backend/.env`:
```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key
LLM_MODEL=gpt-3.5-turbo
```

### Method 2: Docker Compose

Edit `docker-compose.yml`:
```yaml
backend:
  environment:
    LLM_PROVIDER: openai
    LLM_API_KEY: ${OPENAI_API_KEY}
    LLM_MODEL: gpt-3.5-turbo
```

Then set in your shell:
```bash
export OPENAI_API_KEY=sk-your-key
docker-compose up
```

### Method 3: System Environment Variables

```bash
# Linux/Mac
export LLM_PROVIDER=openai
export LLM_API_KEY=sk-your-key
export LLM_MODEL=gpt-3.5-turbo

# Windows
set LLM_PROVIDER=openai
set LLM_API_KEY=sk-your-key
set LLM_MODEL=gpt-3.5-turbo
```

---

## Testing LLM Integration

### 1. Check Logs

After starting the backend, check the logs:

```bash
docker-compose logs backend | grep -i llm
```

You should see:
- `OpenAI client initialized with model: gpt-3.5-turbo` (for OpenAI)
- `Anthropic client initialized with model: claude-3-sonnet-20240229` (for Anthropic)
- `Ollama client initialized with model: llama2` (for Ollama)

### 2. Test via API

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is artificial intelligence?",
    "region": "global"
  }'
```

### 3. Test via Frontend

1. Open http://localhost:3000
2. Type: "Explain quantum computing"
3. You should get a detailed AI-generated response (not a canned response)

---

## Fallback Mode

If no LLM is configured, the system automatically uses fallback mode:

**Indicators of Fallback Mode**:
- Simple, keyword-based responses
- Message saying "I'm currently running in fallback mode"
- Logs show: "Using fallback mode"

**To enable LLM**, configure `LLM_PROVIDER` and `LLM_API_KEY`.

---

## Cost Estimation

### OpenAI Pricing (as of 2024)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| GPT-3.5 Turbo | $0.50 | $1.50 |
| GPT-4 Turbo | $10.00 | $30.00 |
| GPT-4 | $30.00 | $60.00 |

**Example**: 1000 chat messages (500 tokens each) ≈ $0.75 with GPT-3.5

### Anthropic Pricing

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude 3 Haiku | $0.25 | $1.25 |
| Claude 3 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |

### Ollama

**Free!** Runs locally on your machine.

---

## Security Best Practices

### 1. Never Commit API Keys

```bash
# ✅ Good - use environment variables
LLM_API_KEY=${OPENAI_API_KEY}

# ❌ Bad - hardcoded in code
LLM_API_KEY=sk-abc123...
```

### 2. Use Environment Variables

Store API keys in:
- `.env` file (git-ignored)
- System environment variables
- Secret management service (AWS Secrets Manager, etc.)

### 3. Rotate Keys Regularly

- Rotate API keys every 90 days
- Use separate keys for dev/staging/production
- Monitor usage for anomalies

### 4. Rate Limiting

Configure rate limits to prevent abuse:

```python
# In config.py (future enhancement)
MAX_REQUESTS_PER_MINUTE = 60
MAX_TOKENS_PER_REQUEST = 500
```

---

## Troubleshooting

### Issue: "OpenAI client not initialized"

**Cause**: Missing or invalid API key

**Solution**:
```bash
# Check .env file
cat backend/.env | grep LLM_API_KEY

# Verify key starts with sk-
# Get key from: https://platform.openai.com/api-keys
```

### Issue: "Import openai could not be resolved"

**Cause**: Library not installed

**Solution**:
```bash
pip install openai>=1.0.0
# or
docker-compose build backend
```

### Issue: Responses are generic/canned

**Cause**: LLM not configured, running in fallback mode

**Solution**: Set `LLM_PROVIDER` and `LLM_API_KEY` in `.env`

### Issue: "Rate limit exceeded"

**Cause**: Too many API calls

**Solution**:
- Upgrade your OpenAI/Anthropic plan
- Implement caching
- Use a cheaper model (gpt-3.5-turbo instead of gpt-4)

### Issue: Ollama not connecting

**Cause**: Ollama server not running

**Solution**:
```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Pull model if needed
ollama pull llama2
```

---

## Advanced Configuration

### Custom System Prompt

Edit `backend/app/services/chatbot_service.py`:

```python
self.system_prompt = """You are a helpful AI assistant specialized in [YOUR DOMAIN].
Provide clear, accurate responses.
Always cite sources when making factual claims."""
```

### Adjust Temperature

Edit the generation methods in `chatbot_service.py`:

```python
response = self.client.chat.completions.create(
    model=self.llm_model,
    messages=messages,
    max_tokens=500,
    temperature=0.3,  # Lower = more focused, Higher = more creative
)
```

### Add Conversation History (Future Enhancement)

The code already supports conversation history:

```python
def generate_response(self, message: str, conversation_history: Optional[list] = None):
    # conversation_history format:
    # [
    #   {"role": "user", "content": "Hello"},
    #   {"role": "assistant", "content": "Hi there!"},
    #   {"role": "user", "content": "How are you?"}
    # ]
```

To enable, modify `chat.py` to track and pass conversation history.

---

## Provider Comparison

| Feature | OpenAI | Anthropic | Ollama |
|---------|--------|-----------|--------|
| **Cost** | $0.50-60/M tokens | $0.25-75/M tokens | Free |
| **Speed** | Fast | Fast | Varies |
| **Privacy** | Cloud | Cloud | Local |
| **Setup** | Easy | Easy | Medium |
| **Quality** | Excellent | Excellent | Good |
| **Best For** | Production | Production | Development/Privacy |

### Recommendations

- **Development**: Ollama (free, private)
- **Production (Budget)**: OpenAI GPT-3.5 or Claude Haiku
- **Production (Quality)**: OpenAI GPT-4 or Claude Opus
- **Privacy-Sensitive**: Ollama (runs locally)

---

## Migration Guide

### From Fallback to OpenAI

1. Sign up at https://platform.openai.com/
2. Create API key
3. Add to `.env`:
   ```bash
   LLM_PROVIDER=openai
   LLM_API_KEY=sk-your-key
   LLM_MODEL=gpt-3.5-turbo
   ```
4. Restart: `docker-compose restart backend`

### From OpenAI to Anthropic

1. Sign up at https://console.anthropic.com/
2. Create API key
3. Update `.env`:
   ```bash
   LLM_PROVIDER=anthropic
   LLM_API_KEY=sk-ant-your-key
   LLM_MODEL=claude-3-sonnet-20240229
   ```
4. Restart: `docker-compose restart backend`

### From Cloud to Local (Ollama)

1. Install Ollama: https://ollama.ai/
2. Pull model: `ollama pull llama2`
3. Update `.env`:
   ```bash
   LLM_PROVIDER=ollama
   LLM_MODEL=llama2
   # Remove or comment out LLM_API_KEY
   ```
4. Restart: `docker-compose restart backend`

---

## Monitoring & Logging

### Check LLM Provider Status

```bash
# View logs
docker-compose logs backend | grep -i "client initialized"

# Check environment
docker-compose exec backend env | grep LLM
```

### Monitor API Usage

- **OpenAI**: https://platform.openai.com/usage
- **Anthropic**: https://console.anthropic.com/settings/usage
- **Ollama**: No cloud usage (local)

---

## FAQ

**Q: Can I use multiple LLM providers?**
A: Currently, only one provider at a time. Choose via `LLM_PROVIDER` env var.

**Q: Which model should I use?**
A: Start with `gpt-3.5-turbo` (OpenAI) or `claude-3-haiku` (Anthropic) for cost-effectiveness.

**Q: Can I use GPT-4?**
A: Yes, set `LLM_MODEL=gpt-4`, but note it's ~20x more expensive than GPT-3.5.

**Q: How do I use Ollama with Docker?**
A: Ollama needs to run on the host machine. Set `LLM_PROVIDER=ollama` and ensure Ollama is accessible.

**Q: Is my API key secure?**
A: Yes, if you use `.env` files and don't commit them. The `.gitignore` excludes `.env` files.

**Q: Can I customize the prompts?**
A: Yes, edit `system_prompt` in `chatbot_service.py`.

---

## Next Steps

1. ✅ Choose an LLM provider
2. ✅ Configure API key in `.env`
3. ✅ Restart backend
4. ✅ Test with frontend
5. ✅ Monitor usage and costs
6. ✅ Adjust model/temperature as needed

For more help:
- OpenAI Docs: https://platform.openai.com/docs
- Anthropic Docs: https://docs.anthropic.com/
- Ollama Docs: https://ollama.ai/docs

---

**The moderation system will automatically filter all LLM responses before they reach users!** 🛡️
