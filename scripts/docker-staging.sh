#!/bin/bash
# Staging Environment Docker Script
# Usage: ./scripts/docker-staging.sh [up|down|build|logs]

set -e

COMPOSE_FILES="-f docker/docker-compose.yml \
  -f docker/docker-compose.frontend.yml \
  -f docker/docker-compose.backend.yml \
  -f docker/docker-compose.db.yml \
  -f docker/envs/staging.yml"

case "${1:-up}" in
  up)
    echo "Starting staging environment..."
    docker compose $COMPOSE_FILES up -d "${@:2}"
    ;;
  down)
    echo "Stopping staging environment..."
    docker compose $COMPOSE_FILES down "${@:2}"
    ;;
  build)
    echo "Building staging images..."
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
