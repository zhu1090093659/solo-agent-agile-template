#!/bin/bash
# Production Environment Docker Script
# Usage: ./scripts/docker-prod.sh [up|down|build|logs]
#
# Required environment variables:
#   SECRET_KEY    - Application secret key
#   DB_USER       - Database username
#   DB_PASSWORD   - Database password
#   DB_NAME       - Database name

set -e

# Check required environment variables
if [ -z "$SECRET_KEY" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
  echo "Error: Required environment variables not set."
  echo "Please set: SECRET_KEY, DB_USER, DB_PASSWORD, DB_NAME"
  exit 1
fi

COMPOSE_FILES="-f docker/docker-compose.yml \
  -f docker/docker-compose.frontend.yml \
  -f docker/docker-compose.backend.yml \
  -f docker/docker-compose.db.yml \
  -f docker/envs/prod.yml"

case "${1:-up}" in
  up)
    echo "Starting production environment..."
    docker compose $COMPOSE_FILES up -d "${@:2}"
    ;;
  down)
    echo "Stopping production environment..."
    docker compose $COMPOSE_FILES down "${@:2}"
    ;;
  build)
    echo "Building production images..."
    docker compose $COMPOSE_FILES build "${@:2}"
    ;;
  logs)
    docker compose $COMPOSE_FILES logs "${@:2}"
    ;;
  *)
    echo "Usage: $0 [up|down|build|logs]"
    exit 1
    ;;
esac
