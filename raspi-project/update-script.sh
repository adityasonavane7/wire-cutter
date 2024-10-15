#!/bin/bash

# Navigate to the repo directory
cd /path/to/yourrepo

# Fetch the latest changes
git fetch

# Check if there are new commits
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "New updates available, pulling changes..."
  
  # Pull the latest changes
  git pull
  
  # Restart the Docker Compose services
  docker-compose down
  docker-compose up -d --build
  
  echo "Containers restarted with the latest version."
else
  echo "No updates found."
fi