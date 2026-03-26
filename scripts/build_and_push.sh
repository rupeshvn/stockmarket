#!/bin/bash

set -e

# ===== CONFIG =====
IMAGE_NAME="rupeshvn/fastapi-airflow"
PROJECT_DIR="$HOME/Desktop/stockmarket/services/fastapi"

# ===== GENERATE UNIQUE TAG =====
TIMESTAMP=$(date +%Y%m%d%H%M%S)
TAG="$TIMESTAMP"

echo "======================================="
echo "Building image: $IMAGE_NAME:$TAG"
echo "======================================="

# Move to FastAPI directory
cd $PROJECT_DIR

# Build multi-arch image and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $IMAGE_NAME:$TAG \
  -t $IMAGE_NAME:latest \
  --push .

echo "======================================="
echo "Image pushed successfully!"
echo "Tag: $TAG"
echo "======================================="