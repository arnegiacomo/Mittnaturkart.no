#!/bin/bash

# Start frontend in development mode
# Requires: Node.js 20+

cd "$(dirname "$0")"

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Starting frontend on http://localhost:5173"
npm run dev
