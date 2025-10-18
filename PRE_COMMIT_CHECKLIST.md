# Pre-Commit Checklist

Before running the commit scripts, verify these items:

## ✅ Files to KEEP (Should be committed)

### Project Files
- [x] All `.py` files (backend code)
- [x] All `.js`, `.css`, `.html` files (frontend code)
- [x] All `.md` files (documentation)
- [x] `requirements.txt`, `package.json` (dependencies)
- [x] `.env.example` (environment template)
- [x] `.gitignore` (git configuration)
- [x] `Dockerfile`, `docker-compose.yml` (Docker config)
- [x] `.dockerignore` (Docker exclusions)

### Helper Scripts (Useful for others)
- [x] `create_commits.sh` - Commit automation script
- [x] `create_commits.bat` - Windows version
- [x] `GIT_COMMIT_PLAN.md` - Commit strategy documentation
- [x] `HOW_TO_COMMIT.md` - User guide
- [x] `start.sh`, `start.bat` - Convenience startup scripts
- [x] `docker-entrypoint.sh` - Docker initialization

## ❌ Files to EXCLUDE (Already in .gitignore)

### Python Generated Files
- [ ] `__pycache__/` directories
- [ ] `*.pyc`, `*.pyo`, `*.pyd` files
- [ ] `venv/`, `env/`, `ENV/` directories
- [ ] `.Python` files
- [ ] `*.egg-info/` directories

### Node/React Generated Files
- [ ] `node_modules/` directory
- [ ] `frontend/build/` directory
- [ ] `npm-debug.log`, `yarn-error.log`

### Environment & Secrets
- [ ] `.env` file (actual secrets - NEVER commit this!)
- [ ] Any files with actual API keys

### IDE Files
- [ ] `.vscode/` directory
- [ ] `.idea/` directory
- [ ] `*.swp`, `*.swo` files

### Docker/Runtime Files
- [ ] `model_cache/` directory (ML models)
- [ ] `logs/` directory
- [ ] `*.log` files

### Database Files
- [ ] `*.db`, `*.sqlite` files

## 🔍 Verification Steps

### 1. Check for Secrets
```bash
# Search for potential API keys
grep -r "sk-" backend/ --include="*.py" --include="*.env"
grep -r "api_key" backend/ --include="*.py" --include="*.env"
grep -r "password" . --include="*.py" --include="*.env" --include="*.yml"
```

**Expected**: Only references in `.env.example` with placeholder values

### 2. Check .env Files
```bash
# Should NOT exist (should only have .env.example)
ls -la backend/.env
```

**Expected**: File not found (or only placeholders if it exists)

### 3. Verify .gitignore is Working
```bash
git status --ignored
```

**Expected**: Should show ignored files like `node_modules/`, `venv/`, etc.

### 4. Check File Sizes
```bash
# Find large files (over 1MB)
find . -type f -size +1M ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/venv/*"
```

**Expected**: No large binary files (ML models should be in `model_cache/` which is ignored)

### 5. Review Files to be Committed
```bash
# After running create_commits script, check what's included
git ls-files | head -50
```

**Expected**: Only source code, docs, configs - no secrets, no generated files

## 🚨 CRITICAL: Security Check

### Before Pushing to GitHub:

1. **Remove any .env files with real secrets**
   ```bash
   rm backend/.env  # If it has real API keys
   ```

2. **Verify no API keys in code**
   ```bash
   # Search for patterns like sk-, api_key=
   grep -r "sk-[a-zA-Z0-9]" . --include="*.py" --include="*.js"
   ```

3. **Check docker-compose.yml**
   ```bash
   # Ensure no hardcoded secrets
   cat docker-compose.yml | grep -i "key\|password\|secret"
   ```

   Should only see placeholders or `${VARIABLE}` references

4. **Review commit history**
   ```bash
   # After commits are created, review each one
   git log --stat -30
   ```

## 🔒 Recommended: Before First Push

### 1. Create .env with Placeholder Values
If `backend/.env` exists with real values:
```bash
# Backup your real .env
cp backend/.env backend/.env.local.backup

# Copy example as the actual .env (with placeholders)
cp backend/.env.example backend/.env

# The .env.local.backup is ignored by git, but you can use it locally
```

### 2. Update .gitignore (Already Done)
Verify these entries exist:
```
.env
*.env.local
*.env.backup
**/.env
```

### 3. Add Git Secrets Hook (Optional but Recommended)
```bash
# Install git-secrets
# https://github.com/awslabs/git-secrets

git secrets --install
git secrets --register-aws
git secrets --add 'sk-[a-zA-Z0-9]+'
git secrets --add 'api[_-]?key'
```

## ✅ Final Pre-Commit Checklist

- [ ] No `.env` file with real secrets (only `.env.example`)
- [ ] No API keys in code (search completed)
- [ ] No large binary files
- [ ] `.gitignore` is comprehensive
- [ ] `venv/`, `node_modules/` not in repo
- [ ] All documentation is current
- [ ] Reviewed `.gitignore` patterns
- [ ] Tested that Docker can rebuild from scratch
- [ ] No personal information in commits
- [ ] No internal URLs or server names

## 📝 What SHOULD Be Committed

### Backend (`backend/`)
- ✅ All Python source files
- ✅ `requirements.txt`
- ✅ `.env.example` (with placeholders only!)
- ✅ `Dockerfile`, `docker-entrypoint.sh`
- ✅ `.dockerignore`
- ✅ `init_db.py`, `test_api.py`
- ✅ `main.py`

### Frontend (`frontend/`)
- ✅ All JavaScript/React source files
- ✅ All CSS files
- ✅ `package.json`
- ✅ `public/index.html`
- ✅ `Dockerfile`
- ✅ `.dockerignore`

### Root Directory
- ✅ `.gitignore`
- ✅ `README.md` and all `*.md` docs
- ✅ `docker-compose.yml`
- ✅ `start.sh`, `start.bat`
- ✅ `create_commits.sh`, `create_commits.bat`
- ✅ `GIT_COMMIT_PLAN.md`, `HOW_TO_COMMIT.md`

## 🎯 Quick Verification Command

Run this before committing:
```bash
# Check for common issues
echo "Checking for secrets..."
! grep -r "sk-[a-zA-Z0-9]\{20,\}" . --include="*.py" --include="*.js" --exclude-dir=node_modules --exclude-dir=venv

echo "Checking for .env files..."
! find . -name ".env" -not -name ".env.example" -not -path "*/node_modules/*"

echo "Checking for large files..."
! find . -type f -size +5M -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/venv/*" -not -path "*/model_cache/*"

echo "All checks passed! ✅"
```

## 🚀 Ready to Commit?

If all checks pass:
```bash
# Run the commit script
./create_commits.sh  # or create_commits.bat

# Verify
git log --oneline -30
git status

# Push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## 📞 If You Find Issues

### Found a Secret in Code?
1. Remove it
2. Add to `.gitignore`
3. Use environment variables instead
4. Add to `.env.example` as placeholder

### Found Large Files?
1. Remove from repo
2. Add to `.gitignore`
3. Document how to download separately

### Accidentally Committed Secrets?
```bash
# DO NOT just delete and recommit
# GitHub keeps history!

# Use git-filter-branch or BFG Repo-Cleaner
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

---

**Remember: Once pushed to GitHub, assume it's public forever!** 🔒

Always review before pushing!
