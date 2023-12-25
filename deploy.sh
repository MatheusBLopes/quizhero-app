#!/bin/bash

# Variables - replace these with your actual data
USERNAME="orangepi"
ORANGEPI_IP="192.168.100.169"
REPO_PATH="~/apps/quizhero-app/"
DOCKER_IMAGE_NAME="quizhero-app"
GITHUB_REPO_URL="git@github.com:MatheusBLopes/quizhero-app.git"

# SSH into the Orange Pi
ssh $USERNAME@$ORANGEPI_IP << EOF

    # Pull the latest commits from GitHub
    echo "Pulling latest commits from GitHub repository..."
    cd $REPO_PATH
    git pull $GITHUB_REPO_URL

    # Build the Docker image
    echo "Building Docker image..."
    docker build -t $DOCKER_IMAGE_NAME .

    # Run the Docker image
    echo "Running Docker image..."
    docker run -d --name $DOCKER_IMAGE_NAME -p 8000:8000 $DOCKER_IMAGE_NAME

EOF