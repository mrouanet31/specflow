#!/usr/bin/env bash
set -euo pipefail

BACKEND_URL=http://localhost:8080/health
FRONTEND_URL=http://localhost:4200/health

echo "Waiting for services to become ready..."
for i in {1..30}; do
  if curl -fsS --max-time 2 "$BACKEND_URL" >/dev/null; then
    echo "backend ready"
    break
  fi
  sleep 1
done

for i in {1..30}; do
  if curl -fsS --max-time 2 "$FRONTEND_URL" >/dev/null; then
    echo "frontend ready"
    break
  fi
  sleep 1
done

echo "Running smoke checks"
curl -fsS --max-time 5 "$BACKEND_URL" && echo "backend OK"
curl -fsS --max-time 5 "$FRONTEND_URL" && echo "frontend OK"

echo "Smoke tests passed"
