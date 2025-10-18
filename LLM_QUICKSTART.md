# LLM Quick Start - 3 Steps

Get real AI responses in your chatbot in under 5 minutes.

## Option 1: OpenAI (Recommended)

### Step 1: Get API Key
Sign up at https://platform.openai.com/ and create an API key

### Step 2: Configure
Edit `backend/.env`:
```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-openai-api-key-here
LLM_MODEL=gpt-3.5-turbo
```

### Step 3: Restart
```bash
docker-compose restart backend
```

**Done!** Your chatbot now uses GPT-3.5 Turbo. 🎉

---

## Option 2: Anthropic Claude

### Step 1: Get API Key
Sign up at https://console.anthropic.com/

### Step 2: Configure
Edit `backend/.env`:
```bash
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-your-anthropic-key-here
LLM_MODEL=claude-3-sonnet-20240229
```

### Step 3: Restart
```bash
docker-compose restart backend
```

**Done!** Your chatbot now uses Claude 3 Sonnet. 🎉

---

## Option 3: Ollama (Free, Local)

### Step 1: Install Ollama
Download from https://ollama.ai/ and install

### Step 2: Pull Model
```bash
ollama pull llama2
```

### Step 3: Configure
Edit `backend/.env`:
```bash
LLM_PROVIDER=ollama
LLM_MODEL=llama2
# No API key needed!
```

### Step 4: Restart
```bash
docker-compose restart backend
```

**Done!** Your chatbot now uses Llama 2 (running locally). 🎉

---

## Verify It's Working

### Check Logs
```bash
docker-compose logs backend | grep -i "initialized"
```

You should see:
```
OpenAI client initialized with model: gpt-3.5-turbo
```

### Test It
1. Open http://localhost:3000
2. Ask: "Explain quantum computing in simple terms"
3. You should get a detailed, AI-generated response!

---

## No LLM? No Problem!

If you don't configure an LLM:
- ✅ System works fine in fallback mode
- ✅ Returns simple, keyword-based responses
- ✅ All moderation still works
- ✅ Can add LLM later

---

## Quick Comparison

| Provider | Cost | Setup Time | Best For |
|----------|------|------------|----------|
| **OpenAI** | $0.50/M tokens | 2 min | Production |
| **Anthropic** | $0.25-3/M tokens | 2 min | Production |
| **Ollama** | Free | 5 min | Development/Privacy |

---

## Cost Estimate

**OpenAI GPT-3.5:**
- 1,000 messages ≈ $0.75
- 10,000 messages ≈ $7.50
- 100,000 messages ≈ $75

**Anthropic Claude Haiku:**
- 1,000 messages ≈ $0.40
- 10,000 messages ≈ $4.00
- 100,000 messages ≈ $40

**Ollama:**
- Unlimited messages ≈ Free! 🎉

---

## Common Issues

### "Fallback mode" message
→ LLM not configured. Add `LLM_API_KEY` to `.env`

### "Import openai could not be resolved"
→ Run: `docker-compose build backend`

### Ollama connection error
→ Ensure Ollama is running: `ollama list`

---

## Full Documentation

For detailed guides, see:
- [LLM_INTEGRATION.md](LLM_INTEGRATION.md) - Complete integration guide
- [README.md](README.md) - Project overview
- [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Docker deployment

---

## Important: Moderation Still Active! 🛡️

**All LLM responses are automatically moderated** before reaching users:
- ✅ PII detection
- ✅ Toxicity filtering
- ✅ Region-specific rules (GDPR, HIPAA)
- ✅ Custom compliance rules

The LLM generates the response, then the moderation system reviews it!

---

## TL;DR

```bash
# 1. Get API key from OpenAI
# 2. Add to backend/.env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo

# 3. Restart
docker-compose restart backend
```

**That's it!** 🚀
