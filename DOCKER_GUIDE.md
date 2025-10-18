# Docker Deployment Guide

This guide shows you how to run the entire application using Docker - the recommended approach for both development and production.

## Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0 or higher

### Install Docker

**Windows/Mac:**
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

**Linux:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Verify
docker --version
docker compose version
```

## Quick Start (Recommended)

### 1. Start Everything with One Command

```bash
docker-compose up
```

That's it! This single command will:
- ✅ Pull the PostgreSQL image
- ✅ Build the backend container
- ✅ Build the frontend container
- ✅ Create a database
- ✅ Initialize database with seed data
- ✅ Start all services
- ✅ Set up networking between containers

### 2. Access the Application

Once you see the logs showing services are ready:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### 3. Stop Everything

```bash
# Press Ctrl+C in the terminal, then:
docker-compose down
```

## Docker Commands Reference

### Basic Operations

**Start services (foreground):**
```bash
docker-compose up
```

**Start services (background/detached):**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**Stop and remove volumes (clean slate):**
```bash
docker-compose down -v
```

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

**Rebuild containers:**
```bash
docker-compose up --build
```

**Restart a specific service:**
```bash
docker-compose restart backend
```

### Development Workflow

**Watch logs while developing:**
```bash
docker-compose up
# Changes to code will auto-reload (hot reload enabled)
```

**Execute commands in running containers:**
```bash
# Access backend shell
docker-compose exec backend bash

# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d moderation_db

# Run tests
docker-compose exec backend python test_api.py
```

## Container Architecture

```
┌─────────────────────────────────────────────┐
│         Docker Compose Network              │
│                                             │
│  ┌───────────────┐      ┌────────────────┐ │
│  │   Frontend    │      │    Backend     │ │
│  │   (React)     │─────>│   (FastAPI)    │ │
│  │   Port: 3000  │      │   Port: 8000   │ │
│  └───────────────┘      └────────┬───────┘ │
│                                  │         │
│                                  ↓         │
│                         ┌────────────────┐ │
│                         │   PostgreSQL   │ │
│                         │   Port: 5432   │ │
│                         └────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
       ↑                    ↑
       │                    │
   localhost:3000      localhost:8000
```

## Docker Compose Services

### Service: `postgres`
- **Image**: postgres:15
- **Purpose**: Database server
- **Port**: 5432
- **Volume**: `postgres_data` (persistent storage)
- **Health Check**: Ensures DB is ready before starting backend

### Service: `backend`
- **Build**: ./backend
- **Purpose**: FastAPI application
- **Port**: 8000
- **Depends On**: postgres (waits for health check)
- **Volumes**:
  - Code directory (hot reload)
  - `model_cache` (ML models)
- **Auto-initialization**: Database seeded on first run

### Service: `frontend`
- **Build**: ./frontend
- **Purpose**: React application
- **Port**: 3000
- **Depends On**: backend
- **Volumes**: Code directory (hot reload)

## Volumes

Docker Compose creates persistent volumes:

```bash
# List volumes
docker volume ls

# Inspect a volume
docker volume inspect moderation_postgres_data
docker volume inspect moderation_model_cache
```

**Volumes created:**
- `postgres_data` - Database files (persists between restarts)
- `model_cache` - ML models (downloaded once, cached)

## Environment Variables

The `docker-compose.yml` sets these automatically:

```yaml
# Backend
DATABASE_URL: postgresql://postgres:postgres@postgres:5432/moderation_db
SECRET_KEY: your-secret-key-change-in-production
ML_MODEL_CACHE_DIR: /app/model_cache
LOG_LEVEL: INFO

# Frontend
REACT_APP_API_URL: http://localhost:8000
```

**For production**, create a `.env` file:

```bash
# .env
POSTGRES_PASSWORD=secure-password
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/moderation_db
```

Then reference in docker-compose.yml:
```yaml
environment:
  SECRET_KEY: ${SECRET_KEY}
```

## Troubleshooting

### Issue: Port already in use

**Error**: "port is already allocated"

**Solution:**
```bash
# Check what's using the port
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Mac/Linux
lsof -i :8000
lsof -i :3000

# Stop the process or change the port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 on host instead
```

### Issue: Database connection error

**Error**: "could not connect to server"

**Solution:**
```bash
# Check if postgres container is running
docker-compose ps

# Check postgres logs
docker-compose logs postgres

# Restart with clean database
docker-compose down -v
docker-compose up
```

### Issue: Frontend not connecting to backend

**Error**: "Network Error" or CORS error

**Solution:**
```bash
# Ensure backend is running
docker-compose ps

# Check backend logs
docker-compose logs backend

# Verify CORS settings in backend/main.py
```

### Issue: Changes not reflecting

**Problem**: Code changes not appearing

**Solution:**
```bash
# Rebuild the containers
docker-compose up --build

# Or rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

### Issue: ML models downloading slowly

**Problem**: First startup takes long (downloading models)

**Solution:**
- Be patient - models are ~500MB
- Models are cached in `model_cache` volume
- Only happens on first run
- Check progress: `docker-compose logs -f backend`

### Issue: Container crashes or restarts

**Solution:**
```bash
# Check logs for errors
docker-compose logs backend

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart backend

# Full restart
docker-compose down
docker-compose up
```

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- **Backend**: Changes to Python files restart the server automatically
- **Frontend**: Changes to React files rebuild automatically

### Debugging

**Add debugging output:**
```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# All logs
docker-compose logs -f
```

**Access container shell:**
```bash
docker-compose exec backend bash
# Now you're inside the container, can run commands
```

### Running Tests

```bash
# Inside backend container
docker-compose exec backend python test_api.py

# Or start a new container for tests
docker-compose run backend python test_api.py
```

### Database Access

```bash
# Access PostgreSQL CLI
docker-compose exec postgres psql -U postgres -d moderation_db

# Run SQL commands
\dt                                    # List tables
SELECT * FROM moderation_rules;        # Query rules
SELECT COUNT(*) FROM audit_logs;       # Count logs
\q                                     # Exit
```

## Production Deployment

### 1. Security Hardening

**Update docker-compose.yml for production:**

```yaml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}  # Use env var
    # Don't expose port externally
    # Remove: ports: - "5432:5432"

  backend:
    environment:
      SECRET_KEY: ${SECRET_KEY}  # Use secure secret
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/moderation_db
    # Remove volume mounts for code
    # command: uvicorn main:app --host 0.0.0.0 --port 8000  # No --reload
```

### 2. Use Production Dockerfile

Create `backend/Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p model_cache

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

# Production: no reload, multiple workers
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 3. Use Docker Compose Profiles

```yaml
# docker-compose.yml
services:
  backend:
    profiles: ["dev"]
    # dev config

  backend-prod:
    profiles: ["prod"]
    build:
      dockerfile: Dockerfile.prod
    # prod config
```

Run with:
```bash
docker-compose --profile prod up
```

### 4. Add Nginx Reverse Proxy

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
```

## Resource Management

### Limit Resources

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Monitor Resources

```bash
# View resource usage
docker stats

# Specific container
docker stats moderation_backend
```

## Backup and Restore

### Backup Database

```bash
# Backup
docker-compose exec postgres pg_dump -U postgres moderation_db > backup.sql

# Or use docker volume backup
docker run --rm -v moderation_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/db-backup.tar.gz /data
```

### Restore Database

```bash
# Restore
docker-compose exec -T postgres psql -U postgres moderation_db < backup.sql
```

## Advanced Configuration

### Multi-Stage Builds (Optimize Image Size)

```dockerfile
# Build stage
FROM python:3.11 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Checks

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Summary

### Development (Recommended)
```bash
docker-compose up
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cleanup
```bash
docker-compose down -v
```

---

## Quick Command Cheat Sheet

| Task | Command |
|------|---------|
| Start all | `docker-compose up` |
| Start in background | `docker-compose up -d` |
| Stop all | `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Rebuild | `docker-compose up --build` |
| Shell access | `docker-compose exec backend bash` |
| Run tests | `docker-compose exec backend python test_api.py` |
| Database CLI | `docker-compose exec postgres psql -U postgres -d moderation_db` |
| Clean everything | `docker-compose down -v` |
| Check status | `docker-compose ps` |
| View resources | `docker stats` |

---

**With Docker, you get:**
- ✅ One-command startup
- ✅ Consistent environment
- ✅ Easy cleanup
- ✅ Production-ready
- ✅ No manual installation
- ✅ Isolated dependencies
- ✅ Easy scaling

**No more .bat scripts needed - Docker handles everything!** 🐳
