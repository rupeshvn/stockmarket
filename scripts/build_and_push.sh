#!/bin/bash

set -e

# ===== CONFIG =====
FASTAPI_IMAGE="rupeshvn/fastapi-airflow"
AIRFLOW_IMAGE="rupeshvn/airflow-custom"

FASTAPI_DIR="$HOME/Desktop/stockmarket/services/fastapi"
AIRFLOW_DIR="$HOME/Desktop/stockmarket/services/airflow"

# ===== GENERATE UNIQUE TAG =====
TIMESTAMP=$(date +%Y%m%d%H%M%S)
TAG="$TIMESTAMP"

echo "======================================="
echo "Building images with tag: $TAG"
echo "======================================="

# =========================
# 🔹 BUILD FASTAPI IMAGE
# =========================
echo "Building FastAPI image..."

cd $FASTAPI_DIR

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $FASTAPI_IMAGE:$TAG \
  -t $FASTAPI_IMAGE:latest \
  --push .

echo "✅ FastAPI image pushed"

# =========================
# 🔹 BUILD AIRFLOW IMAGE
# =========================
echo "Building Airflow image..."

cd $AIRFLOW_DIR

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $AIRFLOW_IMAGE:$TAG \
  -t $AIRFLOW_IMAGE:latest \
  --push .

echo "✅ Airflow image pushed"

# =========================
# SUMMARY
# =========================
echo "======================================="
echo "All images pushed successfully!"
echo ""
echo "FastAPI: $FASTAPI_IMAGE:$TAG"
echo "Airflow: $AIRFLOW_IMAGE:$TAG"
echo "======================================="