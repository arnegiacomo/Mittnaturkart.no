#!/bin/bash

export VERSION=$(cat VERSION 2>/dev/null || echo "1.0.0")

cd docker
docker compose up -d --build
docker compose ps

echo ""
echo "=================================="
echo "Mittnaturkart v${VERSION}"
echo "=================================="
echo "Frontend:      http://localhost"
echo "API Docs:      http://localhost/docs"
echo "API Base:      http://localhost/api/v1"
echo "Health Check:  http://localhost/health"
echo "=================================="
