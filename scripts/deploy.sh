#!/usr/bin/env bash
# deploy.sh – pull and restart TaskFlow service
# Usage (on remote host or via SSH): ./deploy.sh <image_tag>
# Example: ./deploy.sh ghcr.io/your-org/taskflow:main-abc123
set -euo pipefail
IMAGE_TAG="${1:-}"
APP_NAME="taskflow"
PORT="${PORT:-8000}"

if [[ -z "$IMAGE_TAG" ]]; then
  echo "Usage: $0 <image_tag>"
  exit 1
fi

echo "[deploy] pulling $IMAGE_TAG"
docker pull "$IMAGE_TAG"

# Create a network once; ignore if it exists
docker network create app_net >/dev/null 2>&1 || true
echo "[deploy] stopping old container (if any)"
docker rm -f "$APP_NAME" >/dev/null 2>&1 || true
echo "[deploy] starting new container"

docker run -d \
  --name "$APP_NAME" \
  --restart unless-stopped \
  --network app_net \
  -p 8000:8000 \
  "$IMAGE_TAG"

# Health check
echo "[deploy] waiting for health endpoint..."
for i in {1..20}; do
  if curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null; then
    echo "[deploy] healthy"
    exit 0
  fi
  sleep 1
done

echo "[deploy] health check failed; printing logs"
docker logs "$APP_NAME" || true
exit 1