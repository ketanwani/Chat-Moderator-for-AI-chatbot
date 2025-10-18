#!/bin/bash

# Cleanup script to remove files that shouldn't be committed
# Run this BEFORE running create_commits.sh

echo "=========================================="
echo "Pre-Commit Cleanup Script"
echo "=========================================="
echo ""

# Function to safely remove if exists
safe_remove() {
    if [ -e "$1" ]; then
        echo "Removing: $1"
        rm -rf "$1"
    fi
}

# Function to check if file exists and warn
check_and_warn() {
    if [ -e "$1" ]; then
        echo "⚠️  WARNING: Found $1"
        echo "   This file may contain secrets and should not be committed!"
        echo "   Please review and remove manually if needed."
        echo ""
    fi
}

echo "Step 1: Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type f -name "*.pyd" -delete 2>/dev/null || true
echo "✅ Python cache cleaned"
echo ""

echo "Step 2: Removing virtual environments..."
safe_remove "backend/venv"
safe_remove "backend/env"
safe_remove "backend/ENV"
echo "✅ Virtual environments removed"
echo ""

echo "Step 3: Removing Node modules..."
safe_remove "frontend/node_modules"
echo "✅ Node modules removed"
echo ""

echo "Step 4: Removing build artifacts..."
safe_remove "frontend/build"
safe_remove "backend/build"
safe_remove "backend/dist"
echo "✅ Build artifacts removed"
echo ""

echo "Step 5: Removing logs..."
safe_remove "logs"
find . -type f -name "*.log" -not -path "*/node_modules/*" -delete 2>/dev/null || true
echo "✅ Logs removed"
echo ""

echo "Step 6: Removing model cache..."
safe_remove "backend/model_cache"
echo "✅ Model cache removed (will be downloaded on first run)"
echo ""

echo "Step 7: Removing database files..."
find . -type f -name "*.db" -delete 2>/dev/null || true
find . -type f -name "*.sqlite" -delete 2>/dev/null || true
echo "✅ Database files removed"
echo ""

echo "Step 8: Removing IDE files..."
safe_remove ".vscode"
safe_remove ".idea"
find . -type f -name "*.swp" -delete 2>/dev/null || true
find . -type f -name "*.swo" -delete 2>/dev/null || true
echo "✅ IDE files removed"
echo ""

echo "Step 9: Removing OS files..."
find . -type f -name ".DS_Store" -delete 2>/dev/null || true
find . -type f -name "Thumbs.db" -delete 2>/dev/null || true
echo "✅ OS files removed"
echo ""

echo "=========================================="
echo "Security Checks"
echo "=========================================="
echo ""

echo "Checking for .env files with real secrets..."
check_and_warn "backend/.env"
check_and_warn ".env"

echo "Checking for API keys in code..."
if grep -r "sk-[a-zA-Z0-9]\{20,\}" . --include="*.py" --include="*.js" --exclude-dir=node_modules --exclude-dir=venv 2>/dev/null; then
    echo "⚠️  WARNING: Found potential API keys in code!"
    echo "   Please review and remove before committing."
    echo ""
else
    echo "✅ No API keys found in code"
    echo ""
fi

echo "Checking for large files (>5MB)..."
large_files=$(find . -type f -size +5M -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" -not -path "*/model_cache/*" 2>/dev/null)
if [ -n "$large_files" ]; then
    echo "⚠️  WARNING: Found large files:"
    echo "$large_files"
    echo "   Consider excluding these from git."
    echo ""
else
    echo "✅ No large files found"
    echo ""
fi

echo "=========================================="
echo "Cleanup Summary"
echo "=========================================="
echo ""

echo "Files that WILL be committed:"
echo "  ✅ Source code (.py, .js, .jsx, .css, .html)"
echo "  ✅ Configuration (.env.example, package.json, requirements.txt)"
echo "  ✅ Documentation (.md files)"
echo "  ✅ Docker files (Dockerfile, docker-compose.yml)"
echo "  ✅ Scripts (.sh, .bat)"
echo ""

echo "Files that will NOT be committed (ignored):"
echo "  ❌ .env (secrets)"
echo "  ❌ venv/, node_modules/ (dependencies)"
echo "  ❌ __pycache__/ (Python cache)"
echo "  ❌ *.log (logs)"
echo "  ❌ model_cache/ (ML models)"
echo "  ❌ build/ (build artifacts)"
echo ""

echo "=========================================="
echo "Next Steps"
echo "=========================================="
echo ""
echo "1. Review warnings above (if any)"
echo "2. Manually check backend/.env for secrets"
echo "3. Run: ./create_commits.sh"
echo "4. Push to GitHub"
echo ""

# Check if .env exists and show it
if [ -f "backend/.env" ]; then
    echo "⚠️  IMPORTANT: backend/.env exists!"
    echo ""
    echo "Current content (first 5 lines):"
    head -5 backend/.env
    echo "..."
    echo ""
    echo "Options:"
    echo "  a) If it contains REAL secrets: rm backend/.env"
    echo "  b) If it's just placeholders: it's safe to keep"
    echo "  c) Rename to .env.local: mv backend/.env backend/.env.local"
    echo ""
fi

echo "Ready to commit? Run: ./create_commits.sh"
