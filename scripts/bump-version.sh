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

determine_bump_level() {
    local commit_msg="$1"
    local commit_subject=$(echo "$commit_msg" | head -n 1)
    local commit_body=$(echo "$commit_msg" | tail -n +2)

    if [[ "$commit_subject" =~ ^chore: ]]; then
        echo "none"
    elif [[ "$commit_subject" =~ !: ]] || [[ "$commit_body" =~ BREAKING[[:space:]]CHANGE ]]; then
        echo "major"
    elif [[ "$commit_subject" =~ ^feat: ]] || [[ "$commit_subject" =~ ^feature: ]]; then
        echo "minor"
    elif [[ "$commit_subject" =~ ^fix: ]]; then
        echo "patch"
    else
        echo "patch"
    fi
}

HIGHEST_BUMP="none"

if [ -n "$1" ]; then
    COMMIT_MSG="$1"
    BUMP_LEVEL=$(determine_bump_level "$COMMIT_MSG")
    HIGHEST_BUMP="$BUMP_LEVEL"
    echo "Single commit mode"
    echo "Commit message: $COMMIT_MSG"
    echo "Bump level: $BUMP_LEVEL"
else
    # Find the last version tag
    LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null || echo "")

    if [ -z "$LAST_TAG" ]; then
        echo "No previous version tag found, analyzing all commits"
        COMMIT_HASHES=$(git log --pretty=format:"%H" --reverse)
    else
        echo "Analyzing commits since last tag $LAST_TAG..."
        COMMIT_HASHES=$(git log "$LAST_TAG..HEAD" --pretty=format:"%H" --reverse)
    fi

    if [ -z "$COMMIT_HASHES" ]; then
        echo "No commits found since last tag, using latest commit"
        COMMIT_HASHES=$(git log -1 --pretty=format:"%H")
    fi

    # Analyze each commit by hash
    while IFS= read -r hash; do
        if [ -n "$hash" ]; then
            # Get the full commit message for this hash
            COMMIT_MSG=$(git log -1 --pretty=format:"%B" "$hash")

            BUMP_LEVEL=$(determine_bump_level "$COMMIT_MSG")
            COMMIT_SUBJECT=$(git log -1 --pretty=format:"%s" "$hash")
            echo "Commit: $(echo "$COMMIT_SUBJECT" | cut -c 1-60)..."
            echo "  Bump level: $BUMP_LEVEL"

            if [ "$BUMP_LEVEL" = "major" ]; then
                HIGHEST_BUMP="major"
            elif [ "$BUMP_LEVEL" = "minor" ] && [ "$HIGHEST_BUMP" != "major" ]; then
                HIGHEST_BUMP="minor"
            elif [ "$BUMP_LEVEL" = "patch" ] && [ "$HIGHEST_BUMP" = "none" ]; then
                HIGHEST_BUMP="patch"
            fi
        fi
    done <<< "$COMMIT_HASHES"
fi

echo ""
echo "Highest bump level: $HIGHEST_BUMP"

if [ "$HIGHEST_BUMP" = "none" ]; then
    echo "No version bump needed - skipping"
    exit 0
elif [ "$HIGHEST_BUMP" = "major" ]; then
    echo "Breaking change detected - bumping major version"
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
elif [ "$HIGHEST_BUMP" = "minor" ]; then
    echo "Feature detected - bumping minor version"
    MINOR=$((MINOR + 1))
    PATCH=0
elif [ "$HIGHEST_BUMP" = "patch" ]; then
    echo "Fix detected - bumping patch version"
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
