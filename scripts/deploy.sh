#!/bin/bash

set -e

echo "Pulling latest image..."
docker compose -f compose/docker-compose.prod.yml pull

echo "Starting services..."
docker compose -f compose/docker-compose.prod.yml up -d

echo "Deployment complete."