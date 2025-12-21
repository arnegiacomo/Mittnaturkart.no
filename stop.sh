#!/bin/bash

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
if [ "$RUNNING" -eq 0 ]; then
    echo "No containers running"
    exit 0
fi

echo "Stopping Mittnaturkart v${VERSION}..."
echo ""

if docker compose --env-file ../.env down 2>/dev/null; then
    echo ""
    echo "=================================="
    echo "✓ Application stopped successfully"
    echo "=================================="
    echo ""
    echo "To restart the application, run:"
    echo "  ./start.sh"
    echo ""
else
    echo "Error: Failed to stop containers"
    exit 1
fi
