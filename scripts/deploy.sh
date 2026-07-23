#!/usr/bin/env bash
ENV_FILE="/opt/taskflow/env/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: Missing environment file:"
    echo "  $ENV_FILE"
    exit 1
fi
set -Eeuo pipefail

APP_DIR="/opt/taskflow"
COMPOSE_DIR="$APP_DIR/compose"

echo "========================================="
echo "TaskFlow Deployment Started"
echo "========================================="

cd "$COMPOSE_DIR"

echo "[1/5] Pulling latest images..."
docker compose pull

echo "[2/5] Recreating containers..."
docker compose up -d --remove-orphans

echo "[3/5] Waiting for services..."
sleep 5

echo "[4/5] Container status"
docker compose ps

echo "[5/5] Removing unused images..."
docker image prune -f

echo "Deployment completed successfully."