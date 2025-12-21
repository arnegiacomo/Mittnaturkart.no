#!/bin/bash

export VERSION=$(grep '^version = ' backend/pyproject.toml 2>/dev/null | sed 's/version = "\(.*\)"/\1/' || echo "1.0.0")

echo "Stopping Mittnaturkart v${VERSION}..."
echo ""

cd docker
docker compose down

echo ""
echo "=================================="
echo "✓ Application stopped successfully"
echo "=================================="
echo ""
echo "To restart the application, run:"
echo "  ./start.sh"
echo ""
