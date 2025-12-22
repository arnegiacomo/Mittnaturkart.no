#!/bin/bash

echo "Starting test environment..."

# Run unit tests
echo ""
echo "=========================================="
echo "Running Unit Tests"
echo "=========================================="
docker compose --env-file .env -f docker/docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from unit-test-runner unit-test-runner
UNIT_EXIT_CODE=$?

# Run API tests
echo ""
echo "=========================================="
echo "Running API Tests"
echo "=========================================="
docker compose --env-file .env -f docker/docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test-runner test-runner
API_EXIT_CODE=$?

# Run E2E tests
echo ""
echo "=========================================="
echo "Running E2E Tests"
echo "=========================================="
docker compose --env-file .env -f docker/docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from e2e-runner e2e-runner
E2E_EXIT_CODE=$?

echo ""
echo "Cleaning up test environment..."
docker compose --env-file .env -f docker/docker-compose.test.yml down -v

echo ""
echo "=========================================="
echo "Test Results"
echo "=========================================="
if [ $UNIT_EXIT_CODE -eq 0 ]; then
    echo "✓ Unit Tests: PASSED"
else
    echo "✗ Unit Tests: FAILED"
fi

if [ $API_EXIT_CODE -eq 0 ]; then
    echo "✓ API Tests: PASSED"
else
    echo "✗ API Tests: FAILED"
fi

if [ $E2E_EXIT_CODE -eq 0 ]; then
    echo "✓ E2E Tests: PASSED"
else
    echo "✗ E2E Tests: FAILED"
fi
echo "=========================================="

# Exit with error if any tests failed
if [ $UNIT_EXIT_CODE -ne 0 ] || [ $API_EXIT_CODE -ne 0 ] || [ $E2E_EXIT_CODE -ne 0 ]; then
    exit 1
fi

echo ""
echo "All tests passed!"
