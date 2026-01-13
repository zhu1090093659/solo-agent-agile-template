# Troubleshooting Guide

## Quick Diagnostics

### Health Check Commands

```bash
# Check if services are running
make status

# Check database connection
make db-check

# Check external service connectivity
make check-external

# View recent logs
make logs
```

---

## Common Issues

### Development Environment

#### Issue: Database connection refused

**Symptoms**:
```
Error: Connection refused to localhost:5432
```

**Causes**:
1. Database not running
2. Wrong port configuration
3. Docker container not started

**Solutions**:
```bash
# Check if database is running
docker ps | grep postgres

# Start database
docker-compose up -d db

# Check port configuration
cat .env | grep DATABASE
```

---

#### Issue: Module not found errors

**Symptoms**:
```
ModuleNotFoundError: No module named 'modules'
```

**Causes**:
1. PYTHONPATH not set
2. Virtual environment not activated
3. Dependencies not installed

**Solutions**:
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

---

#### Issue: Tests failing locally but passing in CI

**Symptoms**:
- Tests pass in CI
- Same tests fail locally

**Causes**:
1. Different Python version
2. Missing test database
3. Cached bytecode

**Solutions**:
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Check Python version
python --version

# Reset test database
make db-reset-test
```

---

### Runtime Issues

#### Issue: API returns 500 Internal Server Error

**Symptoms**:
- API endpoint returns 500
- Generic error message

**Diagnosis**:
```bash
# Check application logs
tail -f logs/app.log

# Check for specific error
grep -i "error" logs/app.log | tail -20

# Enable debug mode
DEBUG=true make dev
```

**Common Causes**:
| Cause | Check | Fix |
|-------|-------|-----|
| Database down | `make db-check` | Restart database |
| Missing env var | `env \| grep REQUIRED_VAR` | Add to .env |
| OOM | `docker stats` | Increase memory limit |

---

#### Issue: Slow API response times

**Symptoms**:
- Requests taking > 1 second
- Timeouts occurring

**Diagnosis**:
```bash
# Enable query logging
DATABASE_ECHO=true make dev

# Profile endpoint
curl -w "@curl-format.txt" http://localhost:8000/api/endpoint
```

**Common Causes**:
| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| N+1 queries | Check query log | Add eager loading |
| Missing index | EXPLAIN ANALYZE | Add database index |
| Large payload | Check response size | Add pagination |
| External API | Check external call time | Add caching |

---

#### Issue: Memory usage keeps growing

**Symptoms**:
- Application memory increases over time
- Eventually OOM killed

**Diagnosis**:
```bash
# Monitor memory
docker stats

# Profile memory
python -m memory_profiler src/main.py
```

**Common Causes**:
| Cause | Check | Fix |
|-------|-------|-----|
| Memory leak | Use memory profiler | Fix leak |
| Large cache | Check cache size | Add cache limits |
| Unbounded list | Check data structures | Use generators |

---

### Deployment Issues

#### Issue: Deployment fails

**Symptoms**:
- CI/CD pipeline fails
- Deployment script errors

**Diagnosis**:
```bash
# Check build logs
cat build.log

# Verify build locally
make build

# Check environment variables
printenv | grep -E "^(AWS|DEPLOY|DB)"
```

---

#### Issue: Application crashes after deployment

**Symptoms**:
- Works locally, crashes in production
- Immediate restart loop

**Diagnosis**:
```bash
# Check container logs
kubectl logs -f deployment/app

# Check environment
kubectl exec -it pod/app -- env

# Check resources
kubectl describe pod/app
```

**Common Causes**:
| Cause | Check | Fix |
|-------|-------|-----|
| Missing env var | Compare env files | Add missing vars |
| Wrong DB host | Check DB_HOST | Update config |
| Insufficient memory | Check limits | Increase resources |

---

## Error Code Reference

| Error Code | Meaning | Common Fix |
|------------|---------|------------|
| E001 | Database connection failed | Check database status |
| E002 | Authentication failed | Check credentials |
| E003 | Rate limit exceeded | Wait or increase limit |
| E004 | Invalid input | Check request payload |
| E005 | Resource not found | Verify resource exists |

---

## Log Analysis

### Log Locations

| Environment | Location |
|-------------|----------|
| Local | `logs/` directory |
| Docker | `docker logs container_name` |
| Production | [Log aggregation service] |

### Common Log Patterns

```bash
# Find all errors
grep -i "error\|exception" logs/app.log

# Find specific request
grep "request_id=abc123" logs/app.log

# Count errors by type
grep -i error logs/app.log | sort | uniq -c | sort -rn
```

---

## Getting Help

### Information to Gather

Before asking for help, collect:

1. **Error message** (full stack trace)
2. **Steps to reproduce**
3. **Environment** (local/staging/prod)
4. **Recent changes** (git log --oneline -5)
5. **Relevant logs**

### Escalation Path

1. Check this troubleshooting guide
2. Search existing issues
3. Ask in team channel
4. Create detailed issue

---

## Adding New Entries

When you solve a new issue:

1. Document the symptoms
2. Document the diagnosis steps
3. Document the solution
4. Add to this guide
5. Consider if it indicates a systemic issue to fix
