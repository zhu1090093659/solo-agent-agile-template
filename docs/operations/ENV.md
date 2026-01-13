# Environment Variables

## Overview

This document describes all environment variables used by the application.

---

## Quick Reference

```bash
# Required for all environments
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SECRET_KEY=your-secret-key

# Required for production
[PROD_VAR]=value
```

---

## Variable Categories

### Application

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_ENV` | No | development | Environment: development, staging, production |
| `DEBUG` | No | false | Enable debug mode |
| `LOG_LEVEL` | No | INFO | Logging level: DEBUG, INFO, WARNING, ERROR |
| `PORT` | No | 8000 | HTTP server port |
| `HOST` | No | 0.0.0.0 | HTTP server host |

### Database

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | Full database connection URL |
| `DB_POOL_SIZE` | No | 5 | Connection pool size |
| `DB_POOL_MAX_OVERFLOW` | No | 10 | Max overflow connections |
| `DB_ECHO` | No | false | Log SQL queries |

**DATABASE_URL Format**:
```
postgresql://username:password@host:port/database
```

### Authentication

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | JWT signing key (min 32 chars) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | 30 | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | 7 | Refresh token lifetime |

### External Services

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `[SERVICE]_API_KEY` | Prod | - | API key for [service] |
| `[SERVICE]_API_URL` | No | [default] | API endpoint |

### Email

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SMTP_HOST` | Prod | - | SMTP server host |
| `SMTP_PORT` | No | 587 | SMTP server port |
| `SMTP_USER` | Prod | - | SMTP username |
| `SMTP_PASSWORD` | Prod | - | SMTP password |
| `EMAIL_FROM` | Prod | - | Default from address |

### Storage

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `STORAGE_BACKEND` | No | local | Storage: local, s3, gcs |
| `S3_BUCKET` | If S3 | - | S3 bucket name |
| `S3_REGION` | If S3 | - | AWS region |
| `AWS_ACCESS_KEY_ID` | If S3 | - | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | If S3 | - | AWS secret key |

### Cache

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REDIS_URL` | If Redis | - | Redis connection URL |
| `CACHE_TTL` | No | 3600 | Default cache TTL (seconds) |

---

## Environment-Specific Values

### Development

```bash
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://dev:dev@localhost:5432/app_dev
SECRET_KEY=dev-secret-key-not-for-production
```

### Staging

```bash
APP_ENV=staging
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@staging-db:5432/app_staging
SECRET_KEY=[generated-staging-key]
```

### Production

```bash
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://user:pass@prod-db:5432/app_prod
SECRET_KEY=[generated-production-key]
```

---

## Generating Secrets

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or using openssl
openssl rand -base64 32
```

---

## Validation

The application validates environment variables on startup:

```python
# Required variables must be set
# Type validation (numbers, booleans)
# Format validation (URLs, emails)
```

Missing required variables will cause startup failure with clear error message.

---

## Local Development

### Using .env file

```bash
# Copy example
cp .env.example .env

# Edit with your values
vim .env
```

### Using direnv (recommended)

```bash
# Install direnv
brew install direnv

# Create .envrc
echo "dotenv" > .envrc

# Allow direnv
direnv allow
```

---

## Secrets Management

### Development
- Use `.env` file (never commit!)

### Production
- Use secret management service (e.g., AWS Secrets Manager, HashiCorp Vault)
- Or platform-specific secrets (e.g., Kubernetes Secrets, Vercel Environment Variables)

---

## Adding New Variables

When adding a new environment variable:

1. Add to this document with description
2. Add to `.env.example` with placeholder
3. Add validation in config loading
4. Update deployment configurations
5. Notify team of new requirement
