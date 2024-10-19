#!/bin/bash

LOCAL_REPO_PATH="/home/cmollo/fabai"
cd "$LOCAL_REPO_PATH" || exit

USR_NAME="riwp"
git config --global user.name "$USR_NAME"

E_MAIL="europac197@gmail.com"
git config --global user.email "$E_MAIL"

REPO_NAME="fabai"  # Change this to your desired repository name
gh repo create "$REPO_NAME" --public

ORIGN_URL="https://github.com/riwp/fabai.git"
git remote set-url origin "$ORIGN_URL"

git init
git add .
git commit -m "first commit"
git branch -M main
git push -u origin main


echo "All local files have been pushed successfully."
