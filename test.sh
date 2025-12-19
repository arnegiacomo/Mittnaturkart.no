#!/bin/bash

set -e

echo "Starting test environment..."
docker compose -f docker/docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test-runner

echo ""
echo "Cleaning up test environment..."
docker compose -f docker/docker-compose.test.yml down -v

echo ""
echo "Test run complete!"
