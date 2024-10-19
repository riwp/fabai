#!/bin/bash

# Set the remote repository URL
REPO_URL="git@github.com:riwp/fabai.git"

# Navigate to the project directory
cd "$(dirname "$0")"

# Check if a Git repository exists, and if so, delete it
if [ -d ".git" ]; then
    echo "Existing Git repository found. Removing..."
    rm -rf .git
fi

# Initialize a new Git repository
echo "Initializing new Git repository..."
git init

# Add a .gitignore file if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "*.pyc" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo "node_modules/" >> .gitignore
fi

# Add all files to the new repository
echo "Adding all files to the repository..."
git add .

# Commit the files
read -p "Enter commit message: " commit_message
git commit -m "$commit_message"

# Create a new branch named 'main' (or use 'master' if preferred)
git branch -M main

# Set the remote origin
git remote add origin "$REPO_URL"

# Push to the remote repository
echo "Pushing changes to the remote repository..."
git push -u origin main --force

echo "All local files have been pushed successfully."
