#!/bin/bash

echo "🔐 SECURITY AUDIT - Checking for Exposed API Keys"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check for API keys
check_for_keys() {
    echo -e "\n🔍 Scanning for exposed API keys..."
    
    # API key patterns
    PATTERNS=(
        "AIza[0-9A-Za-z_-]{35}"           # Google API Key
        "sk-[a-zA-Z0-9]{48,}"             # OpenAI API Key  
        "tvly-[a-zA-Z0-9]{32,}"           # Tavily API Key
        "gsk_[a-zA-Z0-9]{56}"             # Google Service Key
        "R3V[a-zA-Z0-9+/]{50,}={0,2}"     # Weaviate API Key pattern
    )
    
    FOUND_ISSUES=false
    
    for pattern in "${PATTERNS[@]}"; do
        echo "  Checking pattern: ${pattern:0:20}..."
        
        # Check staged files
        if git diff --cached --name-only | xargs grep -l "$pattern" 2>/dev/null; then
            echo -e "  ${RED}❌ CRITICAL: API key pattern found in staged files!${NC}"
            FOUND_ISSUES=true
        fi
        
        # Check working directory (excluding .env files)
        if find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" -o -name "*.sh" -o -name "*.json" \) \
           ! -path "./.git/*" ! -name ".env*" ! -name "*.example" \
           -exec grep -l "$pattern" {} \; 2>/dev/null | head -5; then
            echo -e "  ${RED}❌ CRITICAL: API key pattern found in source files!${NC}"
            FOUND_ISSUES=true
        fi
    done
    
    if [ "$FOUND_ISSUES" = false ]; then
        echo -e "  ${GREEN}✅ No API key patterns found in trackable files${NC}"
    fi
}

# Function to check git history
check_git_history() {
    echo -e "\n🕰️  Checking git history for exposed keys..."
    
    if git log --all -p | grep -E "AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{48,}|tvly-[a-zA-Z0-9]{32,}" >/dev/null 2>&1; then
        echo -e "  ${RED}❌ CRITICAL: API keys found in git history!${NC}"
        echo -e "  ${YELLOW}⚠️  Run: ./clean_git_history.sh to clean history${NC}"
        return 1
    else
        echo -e "  ${GREEN}✅ No API keys found in git history${NC}"
        return 0
    fi
}

# Function to check .env file security
check_env_security() {
    echo -e "\n📄 Checking .env file security..."
    
    if [ -f ".env" ]; then
        if git ls-files --error-unmatch .env 2>/dev/null; then
            echo -e "  ${RED}❌ CRITICAL: .env file is tracked by git!${NC}"
            echo -e "  ${YELLOW}⚠️  Run: git rm --cached .env${NC}"
        else
            echo -e "  ${GREEN}✅ .env file is not tracked by git${NC}"
        fi
        
        # Check if .env contains placeholder keys
        if grep -q "YOUR_.*_API_KEY_HERE" .env; then
            echo -e "  ${YELLOW}⚠️  .env contains placeholder keys - update with real keys${NC}"
        else
            echo -e "  ${GREEN}✅ .env appears to contain real API keys${NC}"
        fi
    else
        echo -e "  ${YELLOW}⚠️  No .env file found${NC}"
    fi
}

# Function to check gitignore
check_gitignore() {
    echo -e "\n🚫 Checking .gitignore protection..."
    
    if [ -f ".gitignore" ]; then
        if grep -q ".env" .gitignore; then
            echo -e "  ${GREEN}✅ .env files are ignored${NC}"
        else
            echo -e "  ${RED}❌ .env files are NOT ignored${NC}"
        fi
        
        if grep -q "\*AIza\*" .gitignore; then
            echo -e "  ${GREEN}✅ Google API key patterns are ignored${NC}"
        else
            echo -e "  ${YELLOW}⚠️  Google API key patterns not ignored${NC}"
        fi
    else
        echo -e "  ${RED}❌ No .gitignore file found${NC}"
    fi
}

# Main execution
echo "Starting security audit..."

check_for_keys
HISTORY_CLEAN=$?
check_git_history
check_env_security  
check_gitignore

echo -e "\n🏁 SECURITY AUDIT COMPLETE"
echo "=========================="

if [ $? -eq 0 ] && [ "$FOUND_ISSUES" != true ]; then
    echo -e "${GREEN}✅ Repository appears secure${NC}"
    echo -e "${GREEN}✅ Ready for safe commits and pushes${NC}"
else
    echo -e "${RED}❌ SECURITY ISSUES FOUND${NC}"
    echo -e "${YELLOW}⚠️  DO NOT commit or push until issues are resolved${NC}"
    exit 1
fi
