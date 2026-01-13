# Agent Project: [AGENT_NAME]

> Solo Agent Agile Template - Build AI Agents powered by Claude Code

## Quick Context

[One sentence: What does this Agent do and who is it for?]

**Architecture**: React Frontend → FastAPI Backend → Claude Code CLI → Claude API

## Key Files

| Need | Location |
|------|----------|
| Agent System Prompt | @backend/src/modules/agent/prompts/system.md |
| Agent Service | @backend/src/modules/agent/service.py |
| Claude Code Driver | @backend/src/modules/agent/driver.py |
| Chat API Routes | @backend/src/modules/chat/router.py |
| Chat UI Components | @frontend/src/components/chat/ |
| Current Status | @STATUS.md |
| Roadmap | @ROADMAP.md |

## Commands

```bash
# Development
make install          # Install dependencies
make dev              # Start frontend + backend
make dev-frontend     # Frontend only (port 3000)
make dev-backend      # Backend only (port 8000)

# Claude Code (in project)
/project:context      # Load current work context
/project:next         # Get next task
/project:done "msg"   # Mark task complete
/project:prompt       # Work on agent prompts
```

## Project Structure

```
backend/
  src/
    modules/
      agent/                # 核心 Agent 模块
        driver.py           # Claude Code CLI 驱动
        service.py          # Agent 服务层
        prompts/
          system.md         # 系统提示词 (重要!)
      chat/
        router.py           # Chat API 路由

frontend/
  src/
    components/
      chat/                 # 聊天 UI 组件
    hooks/
      useChat.ts            # SSE 流式 hook
    pages/
      HomePage.tsx          # 聊天界面
```

## Current Focus

> Update this section frequently

**Epic**: [Current Epic Name]
**Task**: [Current Task]
**Status**: [In Progress / Blocked / Done]

## Agent Configuration

### Changing Personality

Edit: `backend/src/modules/agent/prompts/system.md`

### Restricting Tools

In `backend/src/modules/agent/service.py`:
```python
agent_service.set_allowed_tools(["Read", "Write", "Bash"])
```

### Adding Personas

Create: `backend/src/modules/agent/prompts/persona_[name].md`

## API Quick Reference

```bash
# Send message (streaming)
curl -N -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Reload prompt
curl -X POST http://localhost:8000/api/chat/admin/reload-prompt
```

## Gotchas

- Claude Code CLI must be installed: `npm install -g @anthropic-ai/claude-code`
- ANTHROPIC_API_KEY must be set in `.env`
- Each session creates a workspace in `AGENT_WORKSPACE_DIR`

## Quick Start for New Session

```bash
# For NEW projects - initialize based on requirements
/project:init [describe your agent]

# For EXISTING projects - load current context
/project:context

# See what to do next
/project:next
```
