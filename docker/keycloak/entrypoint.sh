#!/bin/bash
set -e

echo "Substituting environment variables in realm template..."
mkdir -p /opt/keycloak/data/import

sed "s|\${KEYCLOAK_REALM}|${KEYCLOAK_REALM}|g; \
     s|\${KEYCLOAK_CLIENT_ID}|${KEYCLOAK_CLIENT_ID}|g; \
     s|\${KEYCLOAK_CLIENT_SECRET}|${KEYCLOAK_CLIENT_SECRET}|g; \
     s|\${FRONTEND_URL}|${FRONTEND_URL}|g" \
     /opt/keycloak/realm-template/realm-export.template.json > /opt/keycloak/data/import/realm-export.json

echo "Starting Keycloak..."
exec /opt/keycloak/bin/kc.sh "$@"
