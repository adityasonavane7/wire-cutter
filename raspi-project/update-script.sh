#!/bin/bash

# Directory where your Git repository is located
REPO_DIR="/etc/wire-cutter/raspi-project"

# Docker Compose file location
DOCKER_COMPOSE_FILE="$REPO_DIR/docker-compose.yml"

# Navigate to the repository directory
cd "$REPO_DIR" || { echo "Repository directory not found!"; exit 1; }

# Fetch latest changes from the remote repo
git fetch

# Get local and remote commit hashes
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

# Compare local and remote hashes
if [ "$LOCAL" != "$REMOTE" ]; then
  echo "$(date): New updates detected. Pulling changes..."
  
  # Pull the latest changes
  git pull
  
  # Stop the currently running containers
  echo "$(date): Stopping current containers..."
  docker-compose -f "$DOCKER_COMPOSE_FILE" down
  
  # Build and start the updated containers
  echo "$(date): Starting updated containers..."
  docker-compose -f "$DOCKER_COMPOSE_FILE" up -d --build

  echo "$(date): Update complete."
else
  echo "$(date): No updates found."
fi