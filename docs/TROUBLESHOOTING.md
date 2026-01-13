# Troubleshooting Guide

## Quick Diagnostics

### Health Check Commands

```bash
# Check if services are running
make status

# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# View logs
make logs
```

---

## Common Issues

### Development Environment

#### Issue: Claude Code CLI not found

**Symptoms**:
```
FileNotFoundError: Claude Code CLI not found
Error: Claude Code CLI not found. Please install: npm install -g @anthropic-ai/claude-code
```

**Solutions**:
```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

---

#### Issue: ANTHROPIC_API_KEY not set

**Symptoms**:
```
Error: ANTHROPIC_API_KEY environment variable not set
```

**Solutions**:
```bash
# Set in .env file
echo "ANTHROPIC_API_KEY=your-key-here" >> backend/.env

# Or export directly
export ANTHROPIC_API_KEY=your-key-here
```

---

#### Issue: Port already in use

**Symptoms**:
```
Error: Address already in use :8000
```

**Solutions**:
```bash
# Find process using port
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Kill process or use different port
PORT=8001 make dev-backend
```

---

#### Issue: Module not found errors

**Symptoms**:
```
ModuleNotFoundError: No module named 'modules'
```

**Solutions**:
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/backend/src"
```

---

### Runtime Issues

#### Issue: SSE stream not working

**Symptoms**:
- No streaming response
- Response arrives all at once
- Connection drops

**Diagnosis**:
```bash
# Test SSE directly
curl -N -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

**Common Causes**:
| Cause | Check | Fix |
|-------|-------|-----|
| Proxy buffering | Check nginx config | Add `proxy_buffering off` |
| CORS | Check browser console | Configure CORS headers |
| Timeout | Check request duration | Increase timeout |

---

#### Issue: Agent timeout

**Symptoms**:
```
Error: Execution timed out after 300s
```

**Solutions**:
```bash
# Increase timeout in settings
AGENT_TIMEOUT=600  # 10 minutes

# Or reduce max turns
AGENT_MAX_TURNS=5
```

---

#### Issue: Workspace permission errors

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
```

**Solutions**:
```bash
# Check workspace directory permissions
ls -la /tmp/agent_workspaces/

# Fix permissions
chmod 755 /tmp/agent_workspaces/

# Or use different workspace directory
AGENT_WORKSPACE_DIR=/path/with/permissions
```

---

### Frontend Issues

#### Issue: CORS errors

**Symptoms**:
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Solutions**:
```python
# In backend main.py, ensure CORS is configured
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### Issue: Chat messages not appearing

**Symptoms**:
- Messages sent but not displayed
- Loading spinner stuck

**Diagnosis**:
1. Check browser console for errors
2. Check network tab for API responses
3. Verify SSE events are being received

---

## Error Code Reference

| Error Code | Meaning | Common Fix |
|------------|---------|------------|
| CLI_NOT_FOUND | Claude Code not installed | Install Claude Code CLI |
| API_KEY_MISSING | No Anthropic API key | Set ANTHROPIC_API_KEY |
| TIMEOUT | Execution took too long | Increase timeout or reduce task |
| SESSION_NOT_FOUND | Invalid session ID | Create new session |
| WORKSPACE_ERROR | File system issue | Check permissions |

---

## Log Analysis

### Log Locations

| Environment | Location |
|-------------|----------|
| Backend | Console output / `logs/` |
| Frontend | Browser console |
| Claude Code | Workspace directory |

### Common Log Patterns

```bash
# Find all errors in backend logs
grep -i "error\|exception" logs/*.log

# Find specific session issues
grep "session_id=abc123" logs/*.log
```

---

## Getting Help

### Information to Gather

Before asking for help, collect:

1. **Error message** (full stack trace)
2. **Steps to reproduce**
3. **Environment** (OS, Python version, Node version)
4. **Configuration** (relevant env vars, sans secrets)
5. **Relevant logs**

### Escalation Path

1. Check this troubleshooting guide
2. Search existing issues on GitHub
3. Check Claude Code documentation
4. Create detailed issue with gathered info

---

## Adding New Entries

When you solve a new issue:

1. Document the symptoms clearly
2. Document the diagnosis steps
3. Document the solution
4. Add to this guide
5. Consider if it indicates a systemic issue to fix
