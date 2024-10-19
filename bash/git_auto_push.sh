#!/bin/bash

# Navigate to the Git repository (change this to your repository path)
cd ~/fabai || { echo "Repository not found"; exit 1; }

# Add all changes to the staging area
git add .

# Check for changes
if ! git diff-index --quiet HEAD --; then
    # Create a commit message with the current date and time
    COMMIT_MESSAGE="Updated on $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Commit the changes
    git commit -m "$COMMIT_MESSAGE"
    
    # Attempt to pull the latest changes from the remote repository
    if git pull origin main --rebase; then
        # Push changes to the remote repository
        git push origin main
        echo "Changes pushed successfully."
    else
        # Check if the error was due to a merge conflict
        if git status | grep -q "both added"; then
            echo "Merge conflict detected. Please resolve conflicts manually."
            echo "After resolving, run 'git add <filename>' and 'git commit' to complete the merge."
            echo "Then, push changes with 'git push origin main'."
        else
            echo "Failed to pull changes from remote. Please resolve conflicts manually."
        fi
    fi
else
    echo "No changes to push."
fi
