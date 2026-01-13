# Development Setup Guide

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| [Language] | [Version] | [Link/command] |
| Docker | 20.10+ | https://docs.docker.com/get-docker/ |
| Make | Any | Usually pre-installed |

### Recommended Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| [IDE/Editor] | Development | [Link] |
| [Tool] | [Purpose] | [Link] |

---

## Quick Start

```bash
# 1. Clone the repository
git clone [repo-url]
cd [project-name]

# 2. Copy environment file
cp .env.example .env

# 3. Install dependencies
make install

# 4. Start development environment
make dev

# 5. Verify setup
make check
```

---

## Detailed Setup

### Step 1: Clone Repository

```bash
git clone [repo-url]
cd [project-name]
```

### Step 2: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your local settings
# See ENV.md for detailed variable descriptions
```

### Step 3: Install Dependencies

```bash
# Create virtual environment (Python)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Or use Make
make install
```

### Step 4: Database Setup

```bash
# Start database container
docker-compose up -d db

# Run migrations
make db-migrate

# (Optional) Seed with sample data
make db-seed
```

### Step 5: Start Development Server

```bash
make dev
```

Application available at: http://localhost:8000

---

## IDE Setup

### VS Code

Recommended extensions:
- [Extension 1]
- [Extension 2]
- [Extension 3]

Settings (`.vscode/settings.json`):
```json
{
    "python.linting.enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}
```

### PyCharm / IntelliJ

1. Open project directory
2. Configure Python interpreter to use `.venv`
3. Mark `src/` as Sources Root

---

## Common Issues During Setup

### Issue: Port already in use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 [PID]

# Or use different port
PORT=8001 make dev
```

### Issue: Database connection fails

```bash
# Check if database is running
docker ps | grep postgres

# Check database logs
docker logs [container-name]

# Restart database
docker-compose restart db
```

### Issue: Permission denied on scripts

```bash
chmod +x scripts/*.sh
```

---

## Verification

Run these commands to verify setup:

```bash
# Run linting
make lint

# Run tests
make test

# Run full check
make check
```

Expected output:
```
All checks passed!
```

---

## Docker Development (Alternative)

If you prefer fully containerized development:

```bash
# Build and start all services
docker-compose up --build

# Run commands in container
docker-compose exec app make test
```

---

## Updating Dependencies

```bash
# Update all dependencies
make update-deps

# Update specific package
pip install --upgrade [package]

# Regenerate lock file
pip-compile requirements.in
```

---

## Cleanup

```bash
# Remove virtual environment
rm -rf .venv

# Remove Docker volumes
docker-compose down -v

# Remove all generated files
make clean
```
