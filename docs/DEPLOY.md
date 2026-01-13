# Deployment Guide

## Deployment Overview

| Environment | Branch | Auto-Deploy | URL |
|-------------|--------|-------------|-----|
| Development | feature/* | No | localhost:8000 |
| Staging | develop | Yes | staging.[domain] |
| Production | main | Manual | [domain] |

---

## Quick Deploy

```bash
# Deploy to staging
make deploy-staging

# Deploy to production
make deploy-prod
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Changelog updated
- [ ] Environment variables configured
- [ ] Claude Agent SDK installed (pip install claude-agent-sdk)

### Post-Deployment

- [ ] Health check passing
- [ ] Smoke tests passing
- [ ] Monitoring alerts configured
- [ ] Team notified

---

## Deployment Methods

### Method 1: Docker (Recommended)

**Using scripts (easiest)**:
```bash
# Windows PowerShell
.\scripts\docker-prod.ps1 build   # Build images
.\scripts\docker-prod.ps1 up      # Deploy

# Linux/macOS/Git Bash
./scripts/docker-prod.sh build
./scripts/docker-prod.sh up
```

**Using compose directly**:
```bash
# Set required environment variables first
export SECRET_KEY="your-secure-secret-key"
export DB_USER="postgres"
export DB_PASSWORD="secure-password"
export DB_NAME="app"

# Build and deploy
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.frontend.yml \
  -f docker/docker-compose.backend.yml \
  -f docker/docker-compose.db.yml \
  -f docker/envs/prod.yml up -d --build
```

<!-- Updated: Docker multi-env deploy - 2026-01-13 -->

### Method 2: Manual Deploy

```bash
# 1. Build frontend
cd frontend
bun run build

# 2. Install backend
cd ../backend
pip install -r requirements.txt

# 3. Start server
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## Environment Configuration

### Required for Production

```bash
# Must be set in production
ANTHROPIC_API_KEY=sk-...
APP_ENV=production
DEBUG=false

# Optional but recommended
AGENT_WORKSPACE_DIR=/var/lib/agent_workspaces
AGENT_MAX_TURNS=10
AGENT_TIMEOUT=300
```

### Secrets Management

- Use environment variables (never commit secrets)
- Use secrets manager in production (AWS Secrets Manager, Vault)
- Rotate API keys regularly

---

## Monitoring After Deploy

### Health Checks

```bash
# Check application health
curl https://[domain]/health

# Expected response
{"status": "healthy"}
```

### Key Metrics to Watch

| Metric | Expected | Alert Threshold |
|--------|----------|-----------------|
| Response time (p95) | < 200ms | > 500ms |
| Error rate | < 0.1% | > 1% |
| Memory usage | < 70% | > 90% |

### Logs

```bash
# View deployment logs
docker-compose logs -f

# Search for errors
docker-compose logs | grep -i error
```

---

## Rollback Procedures

### Application Rollback

```bash
# Rollback to previous version
docker-compose pull [previous-tag]
docker-compose up -d
```

### Quick Rollback

```bash
# If using git tags
git checkout v1.2.3
make deploy-prod
```

---

## Zero-Downtime Deployment

### Strategy: Rolling Update

```
1. Start new instances with new version
2. Wait for health checks to pass
3. Gradually shift traffic to new instances
4. Terminate old instances
```

### Docker Compose Rolling Update

```bash
docker-compose up -d --no-deps --build backend
```

---

## Troubleshooting Deployment

### Build Fails

```bash
# Check build logs
docker-compose build --no-cache

# Common issues:
# - Missing dependencies
# - Incorrect Python/Node version
# - Build script errors
```

### Deploy Fails

```bash
# Check container logs
docker-compose logs backend

# Common issues:
# - Health check fails
# - Missing environment variables
# - Port conflicts
```

### Post-Deploy Issues

```bash
# Immediate rollback if critical
docker-compose down
git checkout [previous-tag]
docker-compose up -d

# Check error logs
docker-compose logs | grep -i "error\|exception"
```

---

## Security Considerations

- Never commit secrets to repository
- Use HTTPS in production
- Configure CORS properly
- Limit agent tool permissions
- Set up workspace cleanup
- Audit deployment access
