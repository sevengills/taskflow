#!/usr/bin/env bash

set -Eeuo pipefail

ENV_FILE="/opt/taskflow/env/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: Missing environment file:"
    echo "  $ENV_FILE"
    exit 1
fi

APP_DIR="/opt/taskflow"
COMPOSE_DIR="$APP_DIR/compose"
COMPOSE_FILE="docker-compose.prod.yml"

echo "========================================="
echo "TaskFlow Deployment Started"
echo "========================================="

cd "$COMPOSE_DIR"

echo "[1/5] Pulling latest images..."
docker compose -f "$COMPOSE_FILE" pull

echo "[2/5] Recreating containers..."
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans

echo "[3/5] Waiting for services..."
sleep 5

echo "[4/5] Container status"
docker compose -f "$COMPOSE_FILE" ps

echo "[5/5] Removing unused images..."
docker image prune -f

echo "Deployment completed successfully."