#!/bin/bash

set -e

PYPROJECT_FILE="backend/pyproject.toml"

if [ ! -f "$PYPROJECT_FILE" ]; then
    echo "Error: $PYPROJECT_FILE not found"
    exit 1
fi

CURRENT_VERSION=$(grep '^version = ' "$PYPROJECT_FILE" | sed 's/version = "\(.*\)"/\1/')
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

sed -i.bak "s/version = \".*\"/version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"
rm "${PYPROJECT_FILE}.bak"
echo "Updated $PYPROJECT_FILE"

if [ -f "frontend/package.json" ]; then
    sed -i.bak "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" frontend/package.json
    rm frontend/package.json.bak
    echo "Updated frontend/package.json"
fi

echo "Version bumped from $CURRENT_VERSION to $NEW_VERSION"
