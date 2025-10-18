@echo off
REM Simplified script to create 11 logical commits
REM Frontend is consolidated into a single commit

echo ==========================================
echo Creating Git Commit Stack (11 commits)
echo ==========================================
echo.

REM Initialize git repository if not already initialized
if not exist ".git" (
    echo Initializing git repository...
    git init
    echo.
)

REM ============================================================================
REM Commit 1: Project Setup
REM ============================================================================

echo [1/11] Initial project setup...
git add .gitignore README.md
git commit -m "chore: initialize project structure" -m "" -m "- Add .gitignore for Python, Node, and IDE files" -m "- Add project README with overview"

REM ============================================================================
REM Commit 2: Backend Foundation
REM ============================================================================

echo [2/11] Backend foundation...
git add backend\requirements.txt backend\.env.example backend\.dockerignore backend\app\__init__.py backend\app\core\ backend\app\db\
git commit -m "feat(backend): add backend foundation and configuration" -m "" -m "- Add requirements.txt with dependencies" -m "- Set up database configuration with SQLAlchemy" -m "- Add environment configuration" -m "- Configure logging and settings"

REM ============================================================================
REM Commit 3: Database Models
REM ============================================================================

echo [3/11] Database models...
git add backend\app\models\ backend\app\schemas\
git commit -m "feat(backend): add database models and schemas" -m "" -m "- Create ModerationRule model with types and regions" -m "- Create AuditLog model for compliance tracking" -m "- Add Pydantic schemas for API validation" -m "- Define enums for rule types (PII, toxicity, etc.)"

REM ============================================================================
REM Commit 4: ML Detection Service
REM ============================================================================

echo [4/11] ML detection service...
git add backend\app\services\ml_detector.py backend\app\services\__init__.py
git commit -m "feat(backend): implement ML-based content detection" -m "" -m "- Add Detoxify model for toxicity detection" -m "- Implement regex-based PII detection" -m "- Add financial and medical term detection" -m "- Support keyword and pattern matching"

REM ============================================================================
REM Commit 5: Chatbot and Moderation Services
REM ============================================================================

echo [5/11] Chatbot and moderation services...
git add backend\app\services\chatbot_service.py backend\app\services\moderation_service.py
git commit -m "feat(backend): add chatbot and core moderation pipeline" -m "" -m "- Create chatbot service with LLM integration" -m "- Support OpenAI, Anthropic, and Ollama providers" -m "- Implement 100%% response interception" -m "- Add priority-based rule execution" -m "- Generate context-aware fallback messages" -m "- Track latency and create audit logs"

REM ============================================================================
REM Commit 6: API Endpoints
REM ============================================================================

echo [6/11] API endpoints...
git add backend\app\api\ backend\main.py
git commit -m "feat(backend): add REST API endpoints" -m "" -m "- Create chat endpoint with moderation" -m "- Add admin CRUD endpoints for rules" -m "- Add audit log query endpoint" -m "- Add statistics endpoint" -m "- Configure CORS and middleware" -m "- Set up health check endpoint"

REM ============================================================================
REM Commit 7: Database Initialization and Testing
REM ============================================================================

echo [7/11] Database init and tests...
git add backend\init_db.py backend\test_api.py
git commit -m "feat(backend): add database initialization and test suite" -m "" -m "- Create init_db.py with 7 default rules" -m "- Add seed data for toxicity, PII, GDPR, HIPAA" -m "- Create comprehensive API test script" -m "- Add latency and moderation tests"

REM ============================================================================
REM Commit 8: Frontend Application (ALL IN ONE)
REM ============================================================================

echo [8/11] Frontend application...
git add frontend\
git commit -m "feat(frontend): add complete React application" -m "" -m "- Set up React project with package.json" -m "- Create main App component with navigation" -m "- Build ChatInterface with message history" -m "- Add region selector for compliance testing" -m "- Create AdminPanel with Rules/Logs/Stats tabs" -m "- Implement rule CRUD operations in UI" -m "- Add moderation status badges and metrics" -m "- Include responsive styling"

REM ============================================================================
REM Commit 9: Docker Configuration
REM ============================================================================

echo [9/11] Docker configuration...
git add backend\Dockerfile backend\docker-entrypoint.sh frontend\Dockerfile frontend\.dockerignore docker-compose.yml
git commit -m "build: add Docker configuration for all services" -m "" -m "- Create Dockerfiles for backend and frontend" -m "- Add docker-compose.yml with all services" -m "- Configure PostgreSQL with health checks" -m "- Set up automatic database initialization" -m "- Add persistent volumes for data and models" -m "- Include docker-entrypoint.sh for setup"

REM ============================================================================
REM Commit 10: Startup Scripts and Helpers
REM ============================================================================

echo [10/11] Startup scripts...
git add start.bat start.sh cleanup_before_commit.bat cleanup_before_commit.sh create_commits.bat create_commits.sh create_commits_simple.bat create_commits_simple.sh
git commit -m "build: add startup and commit helper scripts" -m "" -m "- Add start.bat and start.sh for quick startup" -m "- Add cleanup scripts for pre-commit cleanup" -m "- Add commit automation scripts" -m "- Include both detailed and simplified versions"

REM ============================================================================
REM Commit 11: Documentation
REM ============================================================================

echo [11/11] Documentation...
git add *.md
git commit -m "docs: add comprehensive project documentation" -m "" -m "- Add SETUP.md with installation guide" -m "- Add ARCHITECTURE.md with system design" -m "- Add DOCKER_GUIDE.md and DOCKER_QUICKSTART.md" -m "- Add TESTING.md with test scenarios" -m "- Add LLM_INTEGRATION.md for LLM setup" -m "- Add HOW_TO_COMMIT.md and GIT_COMMIT_PLAN.md" -m "- Add PROJECT_SUMMARY.md and SYSTEM_FLOW.md" -m "- Add QUICK_REFERENCE.md and PRE_COMMIT_CHECKLIST.md"

echo.
echo ==========================================
echo All 11 commits created successfully!
echo ==========================================
echo.
echo Commit Summary:
git log --oneline --no-decorate -11
echo.
echo.
echo Commit Breakdown:
echo   1. Project setup
echo   2. Backend foundation
echo   3. Database models
echo   4. ML detection
echo   5. Chatbot ^& moderation
echo   6. API endpoints
echo   7. DB init ^& tests
echo   8. Frontend (complete)
echo   9. Docker
echo  10. Scripts
echo  11. Documentation
echo.
echo Next Steps:
echo 1. Review commits: git log
echo 2. Add remote: git remote add origin ^<your-repo-url^>
echo 3. Push to GitHub: git push -u origin main
echo.
pause
