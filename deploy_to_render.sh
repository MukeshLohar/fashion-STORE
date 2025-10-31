#!/bin/bash

# Quick Deploy to Render Script
# Run this after making changes to redeploy

echo "🚀 Quick Deploy to Render"
echo "========================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin YOUR_GITHUB_REPO_URL"
    echo "   git push -u origin main"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Uncommitted changes found. Committing..."
    git add .
    read -p "Enter commit message (or press Enter for default): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Update Fashion Store - $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    git commit -m "$commit_msg"
fi

# Push to GitHub (triggers Render deployment)
echo "🔄 Pushing to GitHub..."
git push origin main

echo "✅ Code pushed to GitHub!"
echo "🎯 Render will automatically deploy your changes."
echo "📱 Check deployment status at: https://dashboard.render.com"
echo ""
echo "Your Fashion Store will be available at:"
echo "🌐 https://your-app-name.onrender.com"