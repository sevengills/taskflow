#!/usr/bin/env bash
# rollback.sh — revert TaskFlow container to last stable version
set -euo pipefail
APP_NAME="taskflow"
PREV_IMAGE=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep taskflow | head -n
2 | tail -n 1)
if [[ -z "$PREV_IMAGE" ]]; then
  echo "[ERROR] No previous image found for rollback."
  exit 1
fi
echo "[INFO] Rolling back to $PREV_IMAGE"
docker rm -f "$APP_NAME" >/dev/null 2>&1 || true
docker run -d --name "$APP_NAME" -p 8000:8000 "$PREV_IMAGE"