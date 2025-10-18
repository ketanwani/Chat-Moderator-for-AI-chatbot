@echo off
REM Script to create 30 logical commits for the Moderation Engine project
REM Run this from the project root directory

echo ==========================================
echo Creating Git Commit Stack
echo ==========================================
echo.

REM Initialize git repository if not already initialized
if not exist ".git" (
    echo Initializing git repository...
    git init
    echo.
)

REM ============================================================================
REM Phase 1: Project Foundation (Commits 1-5)
REM ============================================================================

echo Phase 1: Project Foundation (5 commits)
echo ----------------------------------------

REM Commit 1
echo [1/30] Initial project setup...
git add .gitignore README.md
git commit -m "chore: initialize project structure and gitignore" -m "" -m "- Add .gitignore for Python, Node, and common IDE files" -m "- Create root project directory structure" -m "- Add initial README with project overview"

REM Commit 2
echo [2/30] Backend project initialization...
git add backend\requirements.txt backend\main.py backend\.env.example backend\.dockerignore
git commit -m "feat(backend): initialize FastAPI backend structure" -m "" -m "- Set up FastAPI project structure" -m "- Add requirements.txt with core dependencies" -m "- Create main.py with basic FastAPI app" -m "- Add .env.example for environment configuration"

REM Commit 3
echo [3/30] Database configuration...
git add backend\app\db\ backend\app\core\
git commit -m "feat(backend): add database configuration and models setup" -m "" -m "- Configure SQLAlchemy with PostgreSQL" -m "- Add database connection management" -m "- Create base database configuration" -m "- Set up session management"

REM Commit 4
echo [4/30] Moderation rule model...
git add backend\app\models\moderation_rule.py backend\app\models\__init__.py
git commit -m "feat(backend): add moderation rule database model" -m "" -m "- Create ModerationRule model with rule types and regions" -m "- Define enums for RuleType (PII, toxicity, keywords, etc.)" -m "- Define enums for Region (US, EU, Global, etc.)" -m "- Add fields for patterns, thresholds, and priority"

REM Commit 5
echo [5/30] Audit log model...
git add backend\app\models\audit_log.py
git commit -m "feat(backend): add audit log database model" -m "" -m "- Create AuditLog model for compliance tracking" -m "- Add fields for request tracking and moderation results" -m "- Include latency metrics and decision details" -m "- Support session and user tracking"

echo.

REM ============================================================================
REM Phase 2: Core Services (Commits 6-13)
REM ============================================================================

echo Phase 2: Core Services (8 commits)
echo -----------------------------------

REM Commit 6
echo [6/30] Pydantic schemas...
git add backend\app\schemas\
git commit -m "feat(backend): define Pydantic schemas for API validation" -m "" -m "- Add schemas for moderation rules (CRUD)" -m "- Add schemas for chat requests/responses" -m "- Add schemas for audit logs" -m "- Include proper validation and examples"

REM Commit 7
echo [7/30] ML detector service...
git add backend\app\services\ml_detector.py backend\app\services\__init__.py
git commit -m "feat(backend): implement ML-based content detection" -m "" -m "- Add Detoxify model integration for toxicity detection" -m "- Implement regex-based PII detection (email, phone, SSN, etc.)" -m "- Add financial and medical term detection" -m "- Support keyword and regex pattern matching"

REM Commit 8
echo [8/30] Chatbot service...
git add backend\app\services\chatbot_service.py
git commit -m "feat(backend): add chatbot response generation service" -m "" -m "- Create ChatbotService with LLM integration support" -m "- Add fallback responses for when LLM is not configured" -m "- Support OpenAI, Anthropic, and Ollama providers"

REM Commit 9
echo [9/30] Core moderation service...
git add backend\app\services\moderation_service.py
git commit -m "feat(backend): implement core moderation pipeline" -m "" -m "- Create ModerationService with 100%% response interception" -m "- Add priority-based rule execution" -m "- Implement region-specific rule filtering" -m "- Add latency tracking and audit logging" -m "- Generate context-aware fallback messages"

REM Commit 10
echo [10/30] Database initialization...
git add backend\init_db.py
git commit -m "feat(backend): add database initialization with seed data" -m "" -m "- Create init_db.py for database setup" -m "- Add 7 default moderation rules (toxicity, PII, GDPR, HIPAA, etc.)" -m "- Support idempotent initialization" -m "- Include logging for initialization status"

REM Commit 11
echo [11/30] Chat API endpoint...
git add backend\app\api\chat.py backend\app\api\__init__.py
git commit -m "feat(backend): add chat API with moderation integration" -m "" -m "- Create POST /api/v1/chat endpoint" -m "- Integrate chatbot service with moderation pipeline" -m "- Return moderated responses with metadata" -m "- Include latency and flagging information"

REM Commit 12
echo [12/30] Admin API endpoints...
git add backend\app\api\admin.py
git commit -m "feat(backend): add admin APIs for rule management" -m "" -m "- Add CRUD endpoints for moderation rules" -m "- Add audit log query endpoint with filtering" -m "- Add statistics endpoint for monitoring" -m "- Support dynamic rule updates without downtime"

REM Commit 13
echo [13/30] Wire up backend app...
git add backend\app\__init__.py backend\main.py
git commit -m "feat(backend): integrate all services into main FastAPI app" -m "" -m "- Configure CORS middleware" -m "- Register API routers" -m "- Add health check endpoint" -m "- Set up automatic table creation" -m "- Configure logging"

echo.

REM ============================================================================
REM Phase 3: Testing ^& Tools (Commits 14-15)
REM ============================================================================

echo Phase 3: Testing ^& Tools (2 commits)
echo -------------------------------------

REM Commit 14
echo [14/30] API testing script...
git add backend\test_api.py
git commit -m "test(backend): add comprehensive API test suite" -m "" -m "- Create test_api.py for manual testing" -m "- Add tests for all endpoints" -m "- Include latency verification" -m "- Test moderation scenarios (PII, toxicity, etc.)"

REM Commit 15
echo [15/30] Docker for backend...
git add backend\Dockerfile backend\docker-entrypoint.sh
git commit -m "build(backend): add Docker configuration" -m "" -m "- Create Dockerfile for backend container" -m "- Add docker-entrypoint.sh for initialization" -m "- Configure health checks" -m "- Optimize build with .dockerignore"

echo.

REM ============================================================================
REM Phase 4: Frontend (Commits 16-20)
REM ============================================================================

echo Phase 4: Frontend (5 commits)
echo ------------------------------

REM Commit 16
echo [16/30] Initialize React frontend...
git add frontend\package.json frontend\public\ frontend\src\index.js frontend\src\index.css
git commit -m "feat(frontend): initialize React application structure" -m "" -m "- Set up React project with package.json" -m "- Add public HTML template" -m "- Create index.js and basic styling"

REM Commit 17
echo [17/30] Main App component...
git add frontend\src\App.js frontend\src\App.css
git commit -m "feat(frontend): add main App component with navigation" -m "" -m "- Create App component with view routing" -m "- Add header with Chat/Admin toggle" -m "- Include footer" -m "- Add responsive styling"

REM Commit 18
echo [18/30] Chat interface...
git add frontend\src\components\ChatInterface.js frontend\src\components\ChatInterface.css
git commit -m "feat(frontend): build interactive chat interface" -m "" -m "- Create ChatInterface component with message history" -m "- Add region selector for compliance testing" -m "- Implement real-time messaging" -m "- Show moderation status badges" -m "- Display latency metrics"

REM Commit 19
echo [19/30] Admin panel...
git add frontend\src\components\AdminPanel.js frontend\src\components\AdminPanel.css
git commit -m "feat(frontend): create admin dashboard for rule management" -m "" -m "- Add AdminPanel with three-tab interface (Rules, Logs, Stats)" -m "- Implement rule CRUD operations" -m "- Display audit logs with filtering" -m "- Show statistics dashboard with metrics"

REM Commit 20
echo [20/30] Docker for frontend...
git add frontend\Dockerfile frontend\.dockerignore
git commit -m "build(frontend): add Docker configuration" -m "" -m "- Create Dockerfile for frontend container" -m "- Configure for development mode" -m "- Optimize build with .dockerignore"

echo.

REM ============================================================================
REM Phase 5: Docker Orchestration (Commits 21-22)
REM ============================================================================

echo Phase 5: Docker Orchestration (2 commits)
echo ------------------------------------------

REM Commit 21
echo [21/30] Docker Compose...
git add docker-compose.yml
git commit -m "build: add Docker Compose for multi-container setup" -m "" -m "- Create docker-compose.yml with all services" -m "- Configure PostgreSQL with health checks" -m "- Set up backend with auto-initialization" -m "- Configure frontend with proper networking" -m "- Add persistent volumes for data and models"

REM Commit 22
echo [22/30] Startup scripts...
git add start.bat start.sh
git commit -m "build: add convenience scripts for local development" -m "" -m "- Add start.bat for Windows" -m "- Add start.sh for Unix/Mac" -m "- Include automatic setup and initialization"

echo.

REM ============================================================================
REM Phase 6: Documentation (Commits 23-28)
REM ============================================================================

echo Phase 6: Documentation (6 commits)
echo -----------------------------------

REM Commit 23
echo [23/30] Comprehensive README...
git add README.md
git commit -m "docs: create comprehensive project README" -m "" -m "- Add project overview and features" -m "- Include quick start with Docker" -m "- Document tech stack" -m "- Add API endpoints summary" -m "- Include environment configuration"

REM Commit 24
echo [24/30] Setup documentation...
git add SETUP.md
git commit -m "docs: add detailed setup guide" -m "" -m "- Create SETUP.md with step-by-step instructions" -m "- Document prerequisites" -m "- Include database setup" -m "- Add troubleshooting section" -m "- Cover both Docker and manual setup"

REM Commit 25
echo [25/30] Architecture documentation...
git add ARCHITECTURE.md
git commit -m "docs: add architecture documentation" -m "" -m "- Create ARCHITECTURE.md with system design" -m "- Document data flow and components" -m "- Include performance considerations" -m "- Add scalability guidelines"

REM Commit 26
echo [26/30] Docker guides...
git add DOCKER_GUIDE.md DOCKER_QUICKSTART.md
git commit -m "docs: add comprehensive Docker guides" -m "" -m "- Create DOCKER_GUIDE.md with full Docker documentation" -m "- Add DOCKER_QUICKSTART.md for quick reference" -m "- Include troubleshooting and production tips"

REM Commit 27
echo [27/30] Testing and reference docs...
git add TESTING.md QUICK_REFERENCE.md
git commit -m "docs: add testing guide and quick reference" -m "" -m "- Create TESTING.md with test scenarios" -m "- Add QUICK_REFERENCE.md for common commands" -m "- Include API examples and troubleshooting"

REM Commit 28
echo [28/30] Project completion docs...
git add PROJECT_SUMMARY.md PROJECT_COMPLETION.md SYSTEM_FLOW.md
git commit -m "docs: add project summary and system flow diagrams" -m "" -m "- Create PROJECT_SUMMARY.md with features overview" -m "- Add PROJECT_COMPLETION.md with requirements checklist" -m "- Create SYSTEM_FLOW.md with visual diagrams"

echo.

REM ============================================================================
REM Phase 7: LLM Integration ^& Helper Files (Commits 29-30)
REM ============================================================================

echo Phase 7: LLM Integration ^& Helpers (2 commits)
echo -----------------------------------------------

REM Commit 29
echo [29/30] LLM integration docs...
git add LLM_INTEGRATION.md LLM_QUICKSTART.md
git commit -m "docs: add comprehensive LLM integration guides" -m "" -m "- Create LLM_INTEGRATION.md with full setup instructions" -m "- Add LLM_QUICKSTART.md for quick setup" -m "- Include provider comparison and cost estimates" -m "- Add security best practices" -m "- Document troubleshooting steps"

REM Commit 30
echo [30/30] Git workflow helpers...
git add GIT_COMMIT_PLAN.md HOW_TO_COMMIT.md PRE_COMMIT_CHECKLIST.md cleanup_before_commit.bat cleanup_before_commit.sh create_commits.bat create_commits.sh
git commit -m "docs: add Git workflow documentation and helper scripts" -m "" -m "- Add GIT_COMMIT_PLAN.md with commit strategy" -m "- Add HOW_TO_COMMIT.md with step-by-step guide" -m "- Add PRE_COMMIT_CHECKLIST.md for security checks" -m "- Add cleanup scripts for pre-commit cleanup" -m "- Add commit automation scripts"

echo.
echo ==========================================
echo All 30 commits created successfully!
echo ==========================================
echo.
echo Commit Summary:
git log --oneline --no-decorate -30
echo.
echo Next Steps:
echo 1. Review commits: git log
echo 2. Add remote: git remote add origin ^<your-repo-url^>
echo 3. Push to GitHub: git push -u origin main
echo.
echo Or push to a new branch:
echo git checkout -b feature/initial-implementation
echo git push -u origin feature/initial-implementation
echo.
pause
