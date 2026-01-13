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
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Dependencies up to date

### Post-Deployment

- [ ] Health check passing
- [ ] Smoke tests passing
- [ ] Monitoring alerts configured
- [ ] Team notified

---

## Deployment Methods

### Method 1: CI/CD Pipeline (Recommended)

Pipeline runs automatically on merge to deploy branches.

```yaml
# .github/workflows/deploy.yml
deploy:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run tests
      run: make test
    - name: Build
      run: make build
    - name: Deploy
      run: make deploy-${{ env.ENVIRONMENT }}
```

### Method 2: Manual Deploy

```bash
# 1. Build application
make build

# 2. Run migrations
make db-migrate-prod

# 3. Deploy
make deploy-prod

# 4. Verify
make health-check-prod
```

---

## Environment Configuration

### Staging

```bash
# Set environment variables
[PLATFORM] secrets set DATABASE_URL="..."
[PLATFORM] secrets set SECRET_KEY="..."

# Deploy
[PLATFORM] deploy --env staging
```

### Production

```bash
# Set environment variables (use secrets manager)
[PLATFORM] secrets set DATABASE_URL="..."
[PLATFORM] secrets set SECRET_KEY="..."

# Deploy with zero downtime
[PLATFORM] deploy --env production --strategy rolling
```

---

## Database Migrations

### Before Deployment

```bash
# Generate migration
make db-migration "description"

# Test migration locally
make db-migrate
make db-rollback
make db-migrate

# Test migration on staging
make db-migrate-staging
```

### During Deployment

Migrations run automatically as part of deployment.

### Rollback

```bash
# Rollback last migration
make db-rollback-prod

# Rollback to specific version
make db-rollback-prod VERSION=xxx
```

---

## Rollback Procedures

### Application Rollback

```bash
# Rollback to previous version
[PLATFORM] rollback --env production

# Rollback to specific version
[PLATFORM] rollback --env production --version v1.2.3
```

### Database Rollback

```bash
# Only if absolutely necessary
make db-rollback-prod

# Note: Some migrations are not reversible
```

---

## Monitoring After Deploy

### Health Checks

```bash
# Check application health
curl https://[domain]/health

# Expected response
{"status": "healthy", "version": "1.2.3"}
```

### Key Metrics to Watch

| Metric | Expected | Alert Threshold |
|--------|----------|-----------------|
| Response time (p95) | < 200ms | > 500ms |
| Error rate | < 0.1% | > 1% |
| CPU usage | < 50% | > 80% |
| Memory usage | < 70% | > 90% |

### Logs

```bash
# View deployment logs
[PLATFORM] logs --env production --follow

# Search for errors
[PLATFORM] logs --env production --filter "level=error"
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

### Strategy: Blue-Green

```
1. Deploy new version to "green" environment
2. Run smoke tests on green
3. Switch load balancer to green
4. Keep blue as rollback option
```

---

## Hotfix Deployment

For critical production issues:

```bash
# 1. Create hotfix branch from main
git checkout -b hotfix/critical-fix main

# 2. Make minimal fix
# 3. Test thoroughly
make test

# 4. Deploy directly to production
make deploy-prod-hotfix

# 5. Merge back to main and develop
git checkout main && git merge hotfix/critical-fix
git checkout develop && git merge hotfix/critical-fix
```

---

## Deployment Troubleshooting

### Build Fails

```bash
# Check build logs
[PLATFORM] builds --env production

# Common issues:
# - Missing dependencies
# - Incorrect Node/Python version
# - Build script errors
```

### Deploy Fails

```bash
# Check deployment logs
[PLATFORM] deployments --env production

# Common issues:
# - Health check fails
# - Missing environment variables
# - Database connection issues
```

### Post-Deploy Issues

```bash
# Immediate rollback if critical
[PLATFORM] rollback --env production

# Check error logs
[PLATFORM] logs --env production --filter "level=error"

# Check metrics dashboard
# [Link to dashboard]
```

---

## Security Considerations

- Never commit secrets to repository
- Use secrets manager for sensitive values
- Rotate secrets regularly
- Limit deployment access to authorized personnel
- Audit deployment logs
