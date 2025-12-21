#!/bin/bash
set -e

if ! command -v docker &> /dev/null; then
    echo "Error: docker is not installed"
    exit 1
fi

if [ ! -d "docker" ]; then
    echo "Error: Must be run from project root"
    exit 1
fi

export VERSION=$(grep '^version = ' backend/pyproject.toml 2>/dev/null | sed 's/version = "\(.*\)"/\1/' || echo "1.0.0")

cd docker

RUNNING=$(docker compose --env-file ../.env ps -q 2>/dev/null | wc -l | tr -d ' ')
if [ "$RUNNING" -gt 0 ]; then
  echo "Stopping existing containers..."
  docker compose --env-file ../.env down 2>/dev/null || true
  echo ""
fi

if ! docker compose --env-file ../.env up -d --build; then
    echo "Error: Failed to start containers"
    exit 1
fi

docker compose --env-file ../.env ps

echo ""
echo "=================================="
echo "Mittnaturkart v${VERSION}"
echo "=================================="
echo "Frontend:      http://localhost"
echo "API Docs:      http://localhost/docs"
echo "API Base:      http://localhost/api/v1"
echo "Health Check:  http://localhost/health"
echo "Keycloak:      http://localhost/keycloak/admin"
echo "=================================="
