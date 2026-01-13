# Development Setup Guide

> Merged from: SETUP.md, ENV.md, DEPENDENCIES.md

---

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| Python | 3.11+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| Bun | Latest | https://bun.sh/ |
| Docker | 20.10+ | https://docs.docker.com/get-docker/ |

### Recommended Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| VS Code | Development | https://code.visualstudio.com/ |
| Make | Build automation | Usually pre-installed |

---

## Quick Start

```bash
# 1. Clone the repository
git clone [repo-url]
cd [project-name]

# 2. Copy environment file
cp backend/.env.example backend/.env
# Edit backend/.env and add your ANTHROPIC_API_KEY

# 3. Install dependencies (includes Claude Agent SDK)
make install

# 4. Start development environment
make dev

# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

---

## Environment Variables

### Quick Reference

```bash
# Required
ANTHROPIC_API_KEY=your-api-key-here

# Optional with defaults
CLAUDE_MODEL=sonnet
AGENT_WORKSPACE_DIR=/tmp/agent_workspaces
AGENT_MAX_TURNS=10
AGENT_TIMEOUT=300
AGENT_PERMISSION_MODE=acceptEdits
```

### Variable Details

#### Application

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_ENV` | No | development | Environment: development, staging, production |
| `DEBUG` | No | false | Enable debug mode |
| `LOG_LEVEL` | No | INFO | Logging level: DEBUG, INFO, WARNING, ERROR |

#### Agent Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | **Yes** | - | Your Anthropic API key |
| `CLAUDE_MODEL` | No | sonnet | Model: sonnet, opus, haiku |
| `AGENT_WORKSPACE_DIR` | No | /tmp/agent_workspaces | Where Claude SDK runs |
| `AGENT_MAX_TURNS` | No | 10 | Max agentic turns per request |
| `AGENT_TIMEOUT` | No | 300 | Request timeout (seconds) |
| `AGENT_PERMISSION_MODE` | No | acceptEdits | SDK permission mode: default, acceptEdits, bypassPermissions |

#### Server

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HOST` | No | 0.0.0.0 | HTTP server host |
| `PORT` | No | 8000 | HTTP server port |

### Environment-Specific Values

**Development**:
```bash
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
ANTHROPIC_API_KEY=your-dev-key
```

**Production**:
```bash
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
ANTHROPIC_API_KEY=your-prod-key
```

---

## Dependencies

### Core Dependencies

#### FastAPI (Backend)

**Package**: `fastapi`
**Purpose**: Web framework for building APIs

**Why chosen**:
- Async support out of the box
- Automatic OpenAPI documentation
- Type hints for validation

#### React (Frontend)

**Package**: `react`
**Purpose**: UI library

**Why chosen**:
- Component-based architecture
- Large ecosystem
- Good TypeScript support

### Development Dependencies

#### Testing

| Package | Purpose |
|---------|---------|
| pytest | Test runner |
| pytest-asyncio | Async test support |

#### Linting & Formatting

| Package | Purpose |
|---------|---------|
| ruff | Python linter |
| prettier | Frontend formatter |

### External Services

#### Claude Agent SDK

**Package**: `claude-agent-sdk`
**Purpose**: AI agent engine (Python SDK)

**Installation** (included in requirements.txt):
```bash
pip install claude-agent-sdk
```

**Rate limits**: Subject to Anthropic API limits

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
cp backend/.env.example backend/.env

# Edit .env with your settings
# At minimum, set ANTHROPIC_API_KEY
```

### Step 3: Install Dependencies

```bash
# Backend (Python) - includes Claude Agent SDK
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend (Bun/Node)
cd ../frontend
bun install  # or npm install
```

Or use Make:
```bash
make install
```

### Step 4: Start Development Server

```bash
make dev
```

Or start separately:
```bash
# Terminal 1 - Backend
make dev-backend

# Terminal 2 - Frontend
make dev-frontend
```

---

## IDE Setup

### VS Code

Recommended extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- ESLint (dbaeumer.vscode-eslint)
- Tailwind CSS IntelliSense

Settings (`.vscode/settings.json`):
```json
{
    "python.linting.enabled": true,
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

---

## Verification

Run these commands to verify setup:

```bash
# Run linting
make lint

# Run tests
make test

# Check health
curl http://localhost:8000/health
```

---

## Docker Development (Alternative)

```bash
# Build and start all services
docker-compose up --build

# Run commands in container
docker-compose exec backend make test
```

---

## Updating Dependencies

```bash
# Update Python dependencies
pip install --upgrade -r requirements.txt

# Update frontend dependencies
bun update  # or npm update
```

---

## Cleanup

```bash
# Remove virtual environment
rm -rf backend/.venv

# Remove node_modules
rm -rf frontend/node_modules

# Remove Docker volumes
docker-compose down -v

# Full cleanup
make clean
```
