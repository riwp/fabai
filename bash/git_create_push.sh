#!/bin/bash

# Change to the directory of your project
cd /home/cmollo/fabai || exit

# Remove existing git directory if found
if [ -d ".git" ]; then
    echo "Existing Git repository found. Removing..."
    rm -rf .git
fi

# Initialize a new Git repository
echo "Initializing new Git repository..."
git init

# Add all files to the repository
echo "Adding all files to the repository..."
git add .

# Prompt for commit message
#read -p "Enter commit message: " commit_message

# Commit changes
#git commit -m "$commit_message"
git commit -m "init"

# Variables
REPO_NAME="fabai"  # Change this to your desired repository name
GITHUB_USERNAME="riwp"  # Replace with your GitHub username

# Create GitHub repository if it doesn't exist
REPO_CHECK=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME")

if [ "$REPO_CHECK" -eq 404 ]; then
    echo "Repository not found. Creating repository..."
    curl -s -u "$GITHUB_USERNAME" "https://api.github.com/user/repos" -d "{\"name\":\"$REPO_NAME\"}"
else
    echo "Repository already exists."
fi

# Add remote origin using SSH
git remote add origin "git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"

# Push changes to the remote repository
echo "Pushing changes to the remote repository..."
git push -u origin master --force

echo "All local files have been pushed successfully."
