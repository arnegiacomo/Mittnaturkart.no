#!/bin/bash

set -e

VERSION_FILE="VERSION"

if [ ! -f "$VERSION_FILE" ]; then
    echo "1.0.0" > "$VERSION_FILE"
fi

CURRENT_VERSION=$(cat "$VERSION_FILE")
echo "Current version: $CURRENT_VERSION"

IFS='.' read -r -a version_parts <<< "$CURRENT_VERSION"
MAJOR="${version_parts[0]}"
MINOR="${version_parts[1]}"
PATCH="${version_parts[2]}"

COMMIT_MSG="${1:-}"

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG=$(git log -1 --pretty=%B)
fi

echo "Commit message: $COMMIT_MSG"

if [[ "$COMMIT_MSG" =~ ^chore: ]]; then
    echo "Chore commit detected - skipping version bump"
    exit 0
elif [[ "$COMMIT_MSG" =~ ^feat: ]] || [[ "$COMMIT_MSG" =~ ^feature: ]]; then
    echo "Feature commit detected - bumping minor version"
    MINOR=$((MINOR + 1))
    PATCH=0
elif [[ "$COMMIT_MSG" =~ ^fix: ]]; then
    echo "Fix commit detected - bumping patch version"
    PATCH=$((PATCH + 1))
else
    echo "No recognizable commit type - bumping patch version"
    PATCH=$((PATCH + 1))
fi

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "New version: $NEW_VERSION"

echo "$NEW_VERSION" > "$VERSION_FILE"

if [ -f "frontend/package.json" ]; then
    sed -i.bak "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" frontend/package.json
    rm frontend/package.json.bak
    echo "Updated frontend/package.json"
fi

echo "Version bumped from $CURRENT_VERSION to $NEW_VERSION"
