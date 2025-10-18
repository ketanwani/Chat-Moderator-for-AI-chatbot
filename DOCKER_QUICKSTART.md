# Docker Quick Start - 3 Steps to Running

Get the entire application running in under 5 minutes with Docker.

## Prerequisites

Install Docker Desktop:
- **Windows/Mac**: https://www.docker.com/products/docker-desktop
- **Linux**: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

## Step 1: Navigate to Project

```bash
cd "Real Time Moderation and Compliance Engine for AI Chatbot"
```

## Step 2: Start Everything

```bash
docker-compose up
```

**What happens:**
- PostgreSQL database starts (with health checks)
- Backend builds and starts (waits for DB to be ready)
- Database automatically initializes with seed data
- Frontend builds and starts
- All services connect automatically

**First run takes ~2-5 minutes** (downloading ML models and dependencies)
Subsequent runs take ~30 seconds.

## Step 3: Open Browser

Once you see logs showing services are ready:

- **Chat Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## That's It! 🎉

You now have:
- ✅ Frontend running on port 3000
- ✅ Backend running on port 8000
- ✅ PostgreSQL running on port 5432
- ✅ Database initialized with 7 default rules
- ✅ ML models loaded and ready
- ✅ Hot reload enabled (changes reflect automatically)

## Common Commands

**View logs:**
```bash
docker-compose logs -f
```

**Stop services:**
```bash
# Press Ctrl+C, then:
docker-compose down
```

**Restart with fresh database:**
```bash
docker-compose down -v
docker-compose up
```

**Access backend shell:**
```bash
docker-compose exec backend bash
```

**Access database:**
```bash
docker-compose exec postgres psql -U postgres -d moderation_db
```

**Run tests:**
```bash
docker-compose exec backend python test_api.py
```

## Troubleshooting

**Port already in use?**
```bash
# Edit docker-compose.yml and change the port:
ports:
  - "3001:3000"  # Use 3001 instead of 3000
```

**Container not starting?**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Try rebuilding
docker-compose up --build
```

**Database connection error?**
```bash
# Clean restart
docker-compose down -v
docker-compose up
```

## What Containers Are Running?

```bash
docker-compose ps
```

You should see:
- `moderation_db` (PostgreSQL)
- `moderation_backend` (FastAPI)
- `moderation_frontend` (React)

## Stop and Clean Up

**Stop services (keeps data):**
```bash
docker-compose down
```

**Stop and remove all data:**
```bash
docker-compose down -v
```

## Next Steps

1. ✅ Test the chat interface at http://localhost:3000
2. ✅ Try different regions (US, EU, Global)
3. ✅ Switch to Admin Panel to view rules
4. ✅ Check statistics dashboard
5. ✅ View audit logs
6. ✅ Try the API at http://localhost:8000/docs

## Need More Details?

- Full Docker guide: [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
- Setup guide: [SETUP.md](SETUP.md)
- API reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## TL;DR

```bash
# Start
docker-compose up

# Access
http://localhost:3000

# Stop
docker-compose down
```

**No Python, Node.js, or PostgreSQL installation required!** 🚀
