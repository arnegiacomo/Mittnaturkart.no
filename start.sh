#!/bin/bash

export VERSION=$(cat VERSION 2>/dev/null || echo "1.0.0")

cd docker
docker compose up -d --build
docker compose ps
