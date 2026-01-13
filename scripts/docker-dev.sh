#!/bin/bash
# Development Environment Docker Script
# Usage: ./scripts/docker-dev.sh [up|down|build|logs]

set -e

COMPOSE_FILES="-f docker/docker-compose.yml \
  -f docker/docker-compose.frontend.yml \
  -f docker/docker-compose.backend.yml \
  -f docker/docker-compose.db.yml \
  -f docker/envs/dev.yml"

case "${1:-up}" in
  up)
    echo "Starting development environment..."
    docker compose $COMPOSE_FILES up "${@:2}"
    ;;
  down)
    echo "Stopping development environment..."
    docker compose $COMPOSE_FILES down "${@:2}"
    ;;
  build)
    echo "Building development images..."
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
