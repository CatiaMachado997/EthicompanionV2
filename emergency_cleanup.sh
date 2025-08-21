#!/bin/bash

echo "🚨 EMERGENCY SECURITY CLEANUP"
echo "============================="

# The exposed API key that needs to be removed (REDACTED)
EXPOSED_KEY="AIzaSyC3Ke***REDACTED***9mhxBWao"

echo "🔐 Step 1: Stash current changes"
git stash push -m "Security cleanup - stashing changes"

echo "🔐 Step 2: Create replacement file for the exposed key"
echo "$EXPOSED_KEY" > sensitive_data.txt
echo "YOUR_NEW_GOOGLE_API_KEY_HERE" > replacement_data.txt

echo "🔐 Step 3: Use BFG to clean git history"
# Download BFG if not available
if ! command -v bfg &> /dev/null; then
    echo "📥 Downloading BFG Repo Cleaner..."
    curl -L -o bfg.jar https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar
    alias bfg='java -jar bfg.jar'
fi

echo "🧹 Cleaning git history with BFG..."
java -jar bfg.jar --replace-text sensitive_data.txt --no-blob-protection

echo "🔄 Cleaning up git references..."
git reflog expire --expire=now --all && git gc --prune=now --aggressive

echo "🔐 Step 4: Restore stashed changes"
git stash pop

echo "🗑️ Cleaning up temporary files"
rm -f sensitive_data.txt replacement_data.txt bfg.jar

echo ""
echo "✅ Git history cleaned!"
echo ""  
echo "🚨 CRITICAL NEXT STEPS:"
echo "1. Update your .env file with the NEW Google API key"
echo "2. Test that everything still works"
echo "3. Force push to remote: git push --force-with-lease origin master"
echo ""
echo "⚠️  WARNING: This rewrites git history!"
echo "   Anyone with clones of this repo must re-clone it."
