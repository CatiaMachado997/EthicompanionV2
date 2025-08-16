#!/bin/bash

echo "🧹 Cleaning Git History of Exposed API Keys..."

# The exposed key pattern we found
EXPOSED_KEY="AIzaSyC3KetzSrufPXNsvI49-YGFAYO9mhxBWao"

echo "⚠️  WARNING: This will rewrite git history!"
echo "📋 Exposed key to remove: ${EXPOSED_KEY:0:10}...${EXPOSED_KEY: -10}"
echo ""
read -p "Do you want to proceed? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Starting git history cleanup..."
    
    # Use git filter-branch to remove the exposed key from all commits
    git filter-branch --tree-filter '
        find . -type f -name "*.sh" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.md" -o -name "*.txt" -o -name "*.json" | 
        xargs sed -i.bak "s/AIzaSyC3KetzSrufPXNsvI49-YGFAYO9mhxBWao/YOUR_NEW_GOOGLE_API_KEY_HERE/g" 2>/dev/null || true;
        find . -name "*.bak" -delete 2>/dev/null || true
    ' --all
    
    echo "✅ Git history cleaned!"
    echo "🗑️  Cleaning up backup references..."
    
    # Clean up the backup references
    git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
    
    echo "✅ Repository cleanup complete!"
    echo ""
    echo "🚨 IMPORTANT: You MUST force push to update the remote repository:"
    echo "   git push --force-with-lease origin master"
    echo ""
    echo "⚠️  WARNING: This will rewrite the remote git history!"
    echo "   Anyone who has cloned this repo will need to re-clone it."
    
else
    echo "❌ Cleanup cancelled."
fi
