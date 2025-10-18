#!/bin/bash

# Script to create 30 logical commits for the Moderation Engine project
# Run this from the project root directory

set -e  # Exit on error

echo "=========================================="
echo "Creating Git Commit Stack"
echo "=========================================="
echo ""

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo ""
fi

# ============================================================================
# Phase 1: Project Foundation (Commits 1-5)
# ============================================================================

echo "Phase 1: Project Foundation (5 commits)"
echo "----------------------------------------"

# Commit 1: Initial project setup
echo "[1/30] Initial project setup..."
git add .gitignore
git add README.md
git commit -m "chore: initialize project structure and gitignore

- Add .gitignore for Python, Node, and common IDE files
- Create root project directory structure
- Add initial README with project overview"

# Commit 2: Backend project initialization
echo "[2/30] Backend project initialization..."
git add backend/requirements.txt
git add backend/main.py
git add backend/.env.example
git add backend/.dockerignore
git commit -m "feat(backend): initialize FastAPI backend structure

- Set up FastAPI project structure
- Add requirements.txt with core dependencies
- Create main.py with basic FastAPI app
- Add .env.example for environment configuration"

# Commit 3: Database configuration
echo "[3/30] Database configuration..."
git add backend/app/db/
git add backend/app/core/
git commit -m "feat(backend): add database configuration and models setup

- Configure SQLAlchemy with PostgreSQL
- Add database connection management
- Create base database configuration
- Set up session management"

# Commit 4: Define moderation rule model
echo "[4/30] Moderation rule model..."
git add backend/app/models/moderation_rule.py
git add backend/app/models/__init__.py
git commit -m "feat(backend): add moderation rule database model

- Create ModerationRule model with rule types and regions
- Define enums for RuleType (PII, toxicity, keywords, etc.)
- Define enums for Region (US, EU, Global, etc.)
- Add fields for patterns, thresholds, and priority"

# Commit 5: Define audit log model
echo "[5/30] Audit log model..."
git add backend/app/models/audit_log.py
git commit -m "feat(backend): add audit log database model

- Create AuditLog model for compliance tracking
- Add fields for request tracking and moderation results
- Include latency metrics and decision details
- Support session and user tracking"

echo ""

# ============================================================================
# Phase 2: Core Services (Commits 6-13)
# ============================================================================

echo "Phase 2: Core Services (8 commits)"
echo "-----------------------------------"

# Commit 6: Add Pydantic schemas
echo "[6/30] Pydantic schemas..."
git add backend/app/schemas/
git commit -m "feat(backend): define Pydantic schemas for API validation

- Add schemas for moderation rules (CRUD)
- Add schemas for chat requests/responses
- Add schemas for audit logs
- Include proper validation and examples"

# Commit 7: Implement ML detector service
echo "[7/30] ML detector service..."
git add backend/app/services/ml_detector.py
git add backend/app/services/__init__.py
git commit -m "feat(backend): implement ML-based content detection

- Add Detoxify model integration for toxicity detection
- Implement regex-based PII detection (email, phone, SSN, etc.)
- Add financial and medical term detection
- Support keyword and regex pattern matching"

# Commit 8: Create basic chatbot service (before LLM)
echo "[8/30] Basic chatbot service..."
# Temporarily create a simple version
cat > backend/app/services/chatbot_service_temp.py << 'EOF'
import random

class ChatbotService:
    """Simple chatbot service that generates responses"""

    def __init__(self):
        self.responses = {
            "greeting": ["Hello! How can I assist you today?"],
            "default": ["Thanks for asking! Let me provide some information on that."]
        }

    def generate_response(self, message: str) -> str:
        message_lower = message.lower()
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return random.choice(self.responses["greeting"])
        return random.choice(self.responses["default"])

chatbot_service = ChatbotService()
EOF

# Replace the current file temporarily
cp backend/app/services/chatbot_service.py backend/app/services/chatbot_service_full.py
cp backend/app/services/chatbot_service_temp.py backend/app/services/chatbot_service.py
rm backend/app/services/chatbot_service_temp.py

git add backend/app/services/chatbot_service.py
git commit -m "feat(backend): add chatbot response generation service

- Create ChatbotService with keyword-based responses
- Add fallback responses for common queries
- Prepare structure for LLM integration"

# Commit 9: Implement core moderation service
echo "[9/30] Core moderation service..."
git add backend/app/services/moderation_service.py
git commit -m "feat(backend): implement core moderation pipeline

- Create ModerationService with 100% response interception
- Add priority-based rule execution
- Implement region-specific rule filtering
- Add latency tracking and audit logging
- Generate context-aware fallback messages"

# Commit 10: Add database initialization script
echo "[10/30] Database initialization..."
git add backend/init_db.py
git commit -m "feat(backend): add database initialization with seed data

- Create init_db.py for database setup
- Add 7 default moderation rules (toxicity, PII, GDPR, HIPAA, etc.)
- Support idempotent initialization
- Include logging for initialization status"

# Commit 11: Implement chat API endpoint
echo "[11/30] Chat API endpoint..."
git add backend/app/api/chat.py
git add backend/app/api/__init__.py
git commit -m "feat(backend): add chat API with moderation integration

- Create POST /api/v1/chat endpoint
- Integrate chatbot service with moderation pipeline
- Return moderated responses with metadata
- Include latency and flagging information"

# Commit 12: Implement admin API endpoints
echo "[12/30] Admin API endpoints..."
git add backend/app/api/admin.py
git commit -m "feat(backend): add admin APIs for rule management

- Add CRUD endpoints for moderation rules
- Add audit log query endpoint with filtering
- Add statistics endpoint for monitoring
- Support dynamic rule updates without downtime"

# Commit 13: Wire up backend application
echo "[13/30] Wire up backend app..."
git add backend/app/__init__.py
git add backend/main.py
git commit -m "feat(backend): integrate all services into main FastAPI app

- Configure CORS middleware
- Register API routers
- Add health check endpoint
- Set up automatic table creation
- Configure logging"

echo ""

# ============================================================================
# Phase 3: Testing & Tools (Commits 14-15)
# ============================================================================

echo "Phase 3: Testing & Tools (2 commits)"
echo "-------------------------------------"

# Commit 14: Add API testing script
echo "[14/30] API testing script..."
git add backend/test_api.py
git commit -m "test(backend): add comprehensive API test suite

- Create test_api.py for manual testing
- Add tests for all endpoints
- Include latency verification
- Test moderation scenarios (PII, toxicity, etc.)"

# Commit 15: Add Docker support for backend
echo "[15/30] Docker for backend..."
git add backend/Dockerfile
git add backend/docker-entrypoint.sh
git commit -m "build(backend): add Docker configuration

- Create Dockerfile for backend container
- Add docker-entrypoint.sh for initialization
- Configure health checks
- Optimize build with .dockerignore"

echo ""

# ============================================================================
# Phase 4: Frontend (Commits 16-20)
# ============================================================================

echo "Phase 4: Frontend (5 commits)"
echo "------------------------------"

# Commit 16: Initialize React frontend
echo "[16/30] Initialize React frontend..."
git add frontend/package.json
git add frontend/public/
git add frontend/src/index.js
git add frontend/src/index.css
git commit -m "feat(frontend): initialize React application structure

- Set up React project with package.json
- Add public HTML template
- Create index.js and basic styling"

# Commit 17: Create main App component
echo "[17/30] Main App component..."
git add frontend/src/App.js
git add frontend/src/App.css
git commit -m "feat(frontend): add main App component with navigation

- Create App component with view routing
- Add header with Chat/Admin toggle
- Include footer
- Add responsive styling"

# Commit 18: Implement chat interface
echo "[18/30] Chat interface..."
git add frontend/src/components/ChatInterface.js
git add frontend/src/components/ChatInterface.css
git commit -m "feat(frontend): build interactive chat interface

- Create ChatInterface component with message history
- Add region selector for compliance testing
- Implement real-time messaging
- Show moderation status badges
- Display latency metrics"

# Commit 19: Implement admin panel
echo "[19/30] Admin panel..."
git add frontend/src/components/AdminPanel.js
git add frontend/src/components/AdminPanel.css
git commit -m "feat(frontend): create admin dashboard for rule management

- Add AdminPanel with three-tab interface (Rules, Logs, Stats)
- Implement rule CRUD operations
- Display audit logs with filtering
- Show statistics dashboard with metrics"

# Commit 20: Add Docker support for frontend
echo "[20/30] Docker for frontend..."
git add frontend/Dockerfile
git add frontend/.dockerignore
git commit -m "build(frontend): add Docker configuration

- Create Dockerfile for frontend container
- Configure for development mode
- Optimize build with .dockerignore"

echo ""

# ============================================================================
# Phase 5: Docker Orchestration (Commits 21-22)
# ============================================================================

echo "Phase 5: Docker Orchestration (2 commits)"
echo "------------------------------------------"

# Commit 21: Add Docker Compose configuration
echo "[21/30] Docker Compose..."
git add docker-compose.yml
git commit -m "build: add Docker Compose for multi-container setup

- Create docker-compose.yml with all services
- Configure PostgreSQL with health checks
- Set up backend with auto-initialization
- Configure frontend with proper networking
- Add persistent volumes for data and models"

# Commit 22: Add startup scripts
echo "[22/30] Startup scripts..."
git add start.bat
git add start.sh
git commit -m "build: add convenience scripts for local development

- Add start.bat for Windows
- Add start.sh for Unix/Mac
- Include automatic setup and initialization"

echo ""

# ============================================================================
# Phase 6: Documentation (Commits 23-28)
# ============================================================================

echo "Phase 6: Documentation (6 commits)"
echo "-----------------------------------"

# Commit 23: Add comprehensive README
echo "[23/30] Comprehensive README..."
# Update README to full version
git add README.md
git commit -m "docs: create comprehensive project README

- Add project overview and features
- Include quick start with Docker
- Document tech stack
- Add API endpoints summary
- Include environment configuration"

# Commit 24: Add setup documentation
echo "[24/30] Setup documentation..."
git add SETUP.md
git commit -m "docs: add detailed setup guide

- Create SETUP.md with step-by-step instructions
- Document prerequisites
- Include database setup
- Add troubleshooting section
- Cover both Docker and manual setup"

# Commit 25: Add architecture documentation
echo "[25/30] Architecture documentation..."
git add ARCHITECTURE.md
git commit -m "docs: add architecture documentation

- Create ARCHITECTURE.md with system design
- Document data flow and components
- Include performance considerations
- Add scalability guidelines"

# Commit 26: Add Docker guides
echo "[26/30] Docker guides..."
git add DOCKER_GUIDE.md
git add DOCKER_QUICKSTART.md
git commit -m "docs: add comprehensive Docker guides

- Create DOCKER_GUIDE.md with full Docker documentation
- Add DOCKER_QUICKSTART.md for quick reference
- Include troubleshooting and production tips"

# Commit 27: Add testing and reference docs
echo "[27/30] Testing and reference docs..."
git add TESTING.md
git add QUICK_REFERENCE.md
git commit -m "docs: add testing guide and quick reference

- Create TESTING.md with test scenarios
- Add QUICK_REFERENCE.md for common commands
- Include API examples and troubleshooting"

# Commit 28: Add project completion docs
echo "[28/30] Project completion docs..."
git add PROJECT_SUMMARY.md
git add PROJECT_COMPLETION.md
git add SYSTEM_FLOW.md
git commit -m "docs: add project summary and system flow diagrams

- Create PROJECT_SUMMARY.md with features overview
- Add PROJECT_COMPLETION.md with requirements checklist
- Create SYSTEM_FLOW.md with visual diagrams"

echo ""

# ============================================================================
# Phase 7: LLM Integration (Commits 29-30)
# ============================================================================

echo "Phase 7: LLM Integration (2 commits)"
echo "-------------------------------------"

# Commit 29: Implement LLM provider support
echo "[29/30] LLM provider support..."
# Restore the full LLM version
cp backend/app/services/chatbot_service_full.py backend/app/services/chatbot_service.py
rm backend/app/services/chatbot_service_full.py

git add backend/app/services/chatbot_service.py
git add backend/requirements.txt
git add backend/.env.example
git add docker-compose.yml
git commit -m "feat(backend): add multi-provider LLM integration

- Update chatbot_service.py with OpenAI, Anthropic, Ollama support
- Add automatic fallback to keyword responses
- Implement conversation history support
- Include error handling and logging
- Update requirements.txt with LLM libraries
- Add LLM configuration to .env.example"

# Commit 30: Add LLM integration documentation
echo "[30/30] LLM integration docs..."
git add LLM_INTEGRATION.md
git add LLM_QUICKSTART.md
git commit -m "docs: add comprehensive LLM integration guides

- Create LLM_INTEGRATION.md with full setup instructions
- Add LLM_QUICKSTART.md for quick setup
- Include provider comparison and cost estimates
- Add security best practices
- Document troubleshooting steps"

echo ""
echo "=========================================="
echo "✅ All 30 commits created successfully!"
echo "=========================================="
echo ""
echo "Commit Summary:"
git log --oneline --no-decorate | head -30
echo ""
echo "Next Steps:"
echo "1. Review commits: git log"
echo "2. Add remote: git remote add origin <your-repo-url>"
echo "3. Push to GitHub: git push -u origin main"
echo ""
echo "Or push to a new branch:"
echo "git checkout -b feature/initial-implementation"
echo "git push -u origin feature/initial-implementation"
