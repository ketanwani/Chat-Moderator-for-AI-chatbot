#!/bin/bash

# Simplified script to create 11 logical commits
# Frontend is consolidated into a single commit

set -e

echo "=========================================="
echo "Creating Git Commit Stack (11 commits)"
echo "=========================================="
echo ""

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo ""
fi

# ============================================================================
# Commit 1: Project Setup
# ============================================================================

echo "[1/11] Initial project setup..."
git add .gitignore README.md
git commit -m "chore: initialize project structure

- Add .gitignore for Python, Node, and IDE files
- Add project README with overview"

# ============================================================================
# Commit 2: Backend Foundation
# ============================================================================

echo "[2/11] Backend foundation..."
git add backend/requirements.txt backend/.env.example backend/.dockerignore backend/app/__init__.py backend/app/core/ backend/app/db/
git commit -m "feat(backend): add backend foundation and configuration

- Add requirements.txt with dependencies
- Set up database configuration with SQLAlchemy
- Add environment configuration
- Configure logging and settings"

# ============================================================================
# Commit 3: Database Models
# ============================================================================

echo "[3/11] Database models..."
git add backend/app/models/ backend/app/schemas/
git commit -m "feat(backend): add database models and schemas

- Create ModerationRule model with types and regions
- Create AuditLog model for compliance tracking
- Add Pydantic schemas for API validation
- Define enums for rule types (PII, toxicity, etc.)"

# ============================================================================
# Commit 4: ML Detection Service
# ============================================================================

echo "[4/11] ML detection service..."
git add backend/app/services/ml_detector.py backend/app/services/__init__.py
git commit -m "feat(backend): implement ML-based content detection

- Add Detoxify model for toxicity detection
- Implement regex-based PII detection
- Add financial and medical term detection
- Support keyword and pattern matching"

# ============================================================================
# Commit 5: Chatbot and Moderation Services
# ============================================================================

echo "[5/11] Chatbot and moderation services..."
git add backend/app/services/chatbot_service.py backend/app/services/moderation_service.py
git commit -m "feat(backend): add chatbot and core moderation pipeline

- Create chatbot service with LLM integration
- Support OpenAI, Anthropic, and Ollama providers
- Implement 100% response interception
- Add priority-based rule execution
- Generate context-aware fallback messages
- Track latency and create audit logs"

# ============================================================================
# Commit 6: API Endpoints
# ============================================================================

echo "[6/11] API endpoints..."
git add backend/app/api/ backend/main.py
git commit -m "feat(backend): add REST API endpoints

- Create chat endpoint with moderation
- Add admin CRUD endpoints for rules
- Add audit log query endpoint
- Add statistics endpoint
- Configure CORS and middleware
- Set up health check endpoint"

# ============================================================================
# Commit 7: Database Initialization and Testing
# ============================================================================

echo "[7/11] Database init and tests..."
git add backend/init_db.py backend/test_api.py
git commit -m "feat(backend): add database initialization and test suite

- Create init_db.py with 7 default rules
- Add seed data for toxicity, PII, GDPR, HIPAA
- Create comprehensive API test script
- Add latency and moderation tests"

# ============================================================================
# Commit 8: Frontend Application (ALL IN ONE)
# ============================================================================

echo "[8/11] Frontend application..."
git add frontend/
git commit -m "feat(frontend): add complete React application

- Set up React project with package.json
- Create main App component with navigation
- Build ChatInterface with message history
- Add region selector for compliance testing
- Create AdminPanel with Rules/Logs/Stats tabs
- Implement rule CRUD operations in UI
- Add moderation status badges and metrics
- Include responsive styling"

# ============================================================================
# Commit 9: Docker Configuration
# ============================================================================

echo "[9/11] Docker configuration..."
git add backend/Dockerfile backend/docker-entrypoint.sh frontend/Dockerfile frontend/.dockerignore docker-compose.yml
git commit -m "build: add Docker configuration for all services

- Create Dockerfiles for backend and frontend
- Add docker-compose.yml with all services
- Configure PostgreSQL with health checks
- Set up automatic database initialization
- Add persistent volumes for data and models
- Include docker-entrypoint.sh for setup"

# ============================================================================
# Commit 10: Startup Scripts and Helpers
# ============================================================================

echo "[10/11] Startup scripts..."
git add start.bat start.sh cleanup_before_commit.bat cleanup_before_commit.sh create_commits.bat create_commits.sh create_commits_simple.bat create_commits_simple.sh
git commit -m "build: add startup and commit helper scripts

- Add start.bat and start.sh for quick startup
- Add cleanup scripts for pre-commit cleanup
- Add commit automation scripts
- Include both detailed and simplified versions"

# ============================================================================
# Commit 11: Documentation
# ============================================================================

echo "[11/11] Documentation..."
git add *.md
git commit -m "docs: add comprehensive project documentation

- Add SETUP.md with installation guide
- Add ARCHITECTURE.md with system design
- Add DOCKER_GUIDE.md and DOCKER_QUICKSTART.md
- Add TESTING.md with test scenarios
- Add LLM_INTEGRATION.md for LLM setup
- Add HOW_TO_COMMIT.md and GIT_COMMIT_PLAN.md
- Add PROJECT_SUMMARY.md and SYSTEM_FLOW.md
- Add QUICK_REFERENCE.md and PRE_COMMIT_CHECKLIST.md"

echo ""
echo "=========================================="
echo "All 11 commits created successfully!"
echo "=========================================="
echo ""
echo "Commit Summary:"
git log --oneline --no-decorate -11
echo ""
echo ""
echo "Commit Breakdown:"
echo "  1. Project setup"
echo "  2. Backend foundation"
echo "  3. Database models"
echo "  4. ML detection"
echo "  5. Chatbot & moderation"
echo "  6. API endpoints"
echo "  7. DB init & tests"
echo "  8. Frontend (complete)"
echo "  9. Docker"
echo " 10. Scripts"
echo " 11. Documentation"
echo ""
echo "Next Steps:"
echo "1. Review commits: git log"
echo "2. Add remote: git remote add origin <your-repo-url>"
echo "3. Push to GitHub: git push -u origin main"
echo ""
