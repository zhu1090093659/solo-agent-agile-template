# Agent Project: [AGENT_NAME]

> Solo Agent Agile Template - Build AI Agents powered by Claude Agent SDK

## Quick Context

[One sentence: What does this Agent do and who is it for?]

**Architecture**: React Frontend → FastAPI Backend → Claude Agent SDK → Claude API

## Key Files

| Need | Location |
|------|----------|
| Agent System Prompt | @backend/src/modules/agent/prompts/system.md |
| Agent Service | @backend/src/modules/agent/service.py |
| Claude SDK Driver | @backend/src/modules/agent/driver.py |
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
```

### Core Commands (Daily Use)

```bash
/project:context              # Load full work context
/project:context standup      # Standup report format
/project:context brief        # Quick status only

/project:next                 # Get next task recommendation

/project:done "completed X"           # Mark task complete
/project:done "X" --log "notes"       # + record session notes
/project:done "X" --doc               # + update docs

/project:plan "feature"               # Task breakdown
/project:plan "question" --design     # Architecture design
/project:plan "feature" --full        # Design + tasks
```

### Auxiliary Commands (As Needed)

```bash
/project:init "description"           # Initialize new project
/project:init epic "Epic name"        # Create new Epic only

/project:debug "issue"                # Systematic debugging
/project:review                       # Code review
/project:module [name]                # Load module context
```

## Project Structure

```
backend/
  src/
    modules/
      agent/                # 核心 Agent 模块
        driver.py           # Claude Agent SDK 驱动
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

- Claude Agent SDK must be installed: `pip install claude-agent-sdk`
- ANTHROPIC_API_KEY must be set in `.env`
- Each session creates a workspace in `AGENT_WORKSPACE_DIR`

## Quick Start for New Session

```bash
# For NEW projects - initialize based on requirements
/project:init [describe your agent]

# For EXISTING projects - load current context
/project:context              # Full context
/project:context brief        # Quick status

# See what to do next
/project:next

# After completing a task
/project:done "what you completed"
```
