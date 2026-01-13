.PHONY: help install dev test lint format check clean build deploy

# Default target
help:
	@echo "Solo Agile Project Commands (React + FastAPI)"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install all dependencies"
	@echo "  make install-frontend Install frontend only"
	@echo "  make install-backend  Install backend only"
	@echo "  make setup            Full setup (install + db)"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Start both frontend and backend"
	@echo "  make dev-frontend     Start frontend only (port 3000)"
	@echo "  make dev-backend      Start backend only (port 8000)"
	@echo "  make test             Run all tests"
	@echo "  make lint             Run all linters"
	@echo "  make format           Format all code"
	@echo "  make check            Run all checks"
	@echo ""
	@echo "Database:"
	@echo "  make db-start         Start database container"
	@echo "  make db-stop          Stop database container"
	@echo "  make db-migrate       Run migrations"
	@echo "  make db-reset         Reset database"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  make build            Build for production"
	@echo "  make build-frontend   Build frontend only"
	@echo "  make deploy-staging   Deploy to staging"
	@echo "  make deploy-prod      Deploy to production"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            Clean build artifacts"
	@echo "  make status           Show project status"

# ============================================================
# Setup
# ============================================================

install: install-backend install-frontend
	@echo "All dependencies installed."

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && bun install
	@echo "Frontend ready."

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv .venv || true
	cd backend && . .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt
	@echo "Backend ready."

setup: install db-start db-migrate
	@echo "Setup complete."

# ============================================================
# Development
# ============================================================

dev:
	@echo "Starting development servers..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/docs"
	@$(MAKE) -j2 dev-frontend dev-backend

dev-frontend:
	@echo "Starting frontend..."
	cd frontend && bun run dev

dev-backend:
	@echo "Starting backend..."
	cd backend && . .venv/bin/activate && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# ============================================================
# Testing
# ============================================================

test: test-backend test-frontend
	@echo "All tests passed."

test-backend:
	@echo "Running backend tests..."
	cd backend && . .venv/bin/activate && pytest tests/ -v --cov=src --cov-report=term-missing

test-frontend:
	@echo "Running frontend type check..."
	cd frontend && bun run typecheck

test-unit:
	@echo "Running backend unit tests..."
	cd backend && . .venv/bin/activate && pytest tests/unit/ -v

test-integration:
	@echo "Running integration tests..."
	cd backend && . .venv/bin/activate && pytest tests/integration/ -v

# ============================================================
# Linting & Formatting
# ============================================================

lint: lint-backend lint-frontend
	@echo "All linting passed."

lint-backend:
	@echo "Linting backend..."
	cd backend && . .venv/bin/activate && ruff check src/ tests/
	cd backend && . .venv/bin/activate && mypy src/

lint-frontend:
	@echo "Linting frontend..."
	cd frontend && bun run lint
	cd frontend && bun run typecheck

format: format-backend format-frontend
	@echo "All code formatted."

format-backend:
	@echo "Formatting backend..."
	cd backend && . .venv/bin/activate && ruff format src/ tests/
	cd backend && . .venv/bin/activate && ruff check --fix src/ tests/

format-frontend:
	@echo "Formatting frontend..."
	cd frontend && bun run format

check: lint test
	@echo "All checks passed."

# ============================================================
# Database
# ============================================================

db-start:
	@echo "Starting database..."
	docker-compose up -d db

db-stop:
	@echo "Stopping database..."
	docker-compose stop db

db-migrate:
	@echo "Running migrations..."
	cd backend && . .venv/bin/activate && alembic upgrade head

db-rollback:
	@echo "Rolling back last migration..."
	cd backend && . .venv/bin/activate && alembic downgrade -1

db-reset:
	@echo "Resetting database..."
	docker-compose down -v db
	docker-compose up -d db
	sleep 3
	cd backend && . .venv/bin/activate && alembic upgrade head

db-status:
	@echo "Database migration status:"
	cd backend && . .venv/bin/activate && alembic current

# ============================================================
# Build & Deploy
# ============================================================

build: build-frontend build-backend
	@echo "Build complete."

build-frontend:
	@echo "Building frontend..."
	cd frontend && bun run build
	@echo "Frontend built to frontend/dist/"

build-backend:
	@echo "Building backend Docker image..."
	cd backend && docker build -t backend:latest .

deploy-staging:
	@echo "Deploying to staging..."
	# Add your staging deployment commands here
	@echo "Deployed to staging."

deploy-prod:
	@echo "Deploying to production..."
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	# Add your production deployment commands here
	@echo "Deployed to production."

# ============================================================
# Utilities
# ============================================================

clean:
	@echo "Cleaning build artifacts..."
	# Backend
	find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find backend -type f -name "*.pyc" -delete
	find backend -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find backend -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find backend -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	# Frontend
	rm -rf frontend/dist frontend/node_modules/.cache
	@echo "Done."

logs:
	@echo "Showing backend logs..."
	cd backend && tail -f logs/app.log

# ============================================================
# Project Info
# ============================================================

status:
	@echo "=== Project Status ==="
	@cat STATUS.md | head -30
	@echo ""
	@echo "=== Git Status ==="
	@git status --short 2>/dev/null || echo "Not a git repository"
