# Agent Project: [AGENT_NAME]

> Solo Agent Agile Template - Build AI Agents powered by Claude Agent SDK

## Quick Context

[One sentence: What does this Agent do and who is it for?]

**Architecture**: React Frontend -> FastAPI Backend -> Claude Agent SDK -> Claude API

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
| Learnings | @docs/LEARNINGS.md |

## Project Structure

```
backend/
  src/
    modules/
      agent/                # Core Agent module
        driver.py           # Claude Agent SDK driver
        service.py          # Agent service layer
        prompts/
          system.md         # System prompt (important!)
      chat/
        router.py           # Chat API routes

frontend/
  src/
    components/
      chat/                 # Chat UI components
    hooks/
      useChat.ts            # SSE streaming hook
    pages/
      HomePage.tsx          # Chat page
```

## Current Focus

> Update this section frequently

**Epic**: [Current Epic Name]
**Task**: [Current Task]
**Status**: [In Progress / Blocked / Done]

---

## Working Rules

### 1. Filesystem as External Memory

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
```

Important information MUST be written to files, not just kept in conversation:
- Research findings -> notes.md
- Errors encountered -> docs/LEARNINGS.md
- Decisions made -> notes.md or ADR

### 2. 2-Action Rule

After every 2 "view" operations, save findings to notes.md:
- Read file + Search -> Save findings
- Run tests + Check logs -> Save findings

This prevents losing important discoveries.

### 3. Re-read Plan Before Major Decisions

Before architecture decisions or starting new phases:
- Re-read STATUS.md to confirm current state
- Re-read current Epic's EPIC.md to confirm goal
- Check docs/LEARNINGS.md to avoid repeating mistakes

### 4. Record All Errors

When encountering errors, immediately record to docs/LEARNINGS.md:
- Do NOT wait until "after it's fixed"
- Include: Problem, Cause, Solution
- Helps avoid repeating the same mistakes

### 5. Active Task Tracking

For medium complexity tasks (3-10 steps):
- Create Active Task section in notes.md
- Track phase progress and findings
- Archive to Session Log when complete

## Task Complexity Guide

| Complexity | Steps | Approach |
|------------|-------|----------|
| Simple | <3 | Execute directly |
| Medium | 3-10 | Create Active Task in notes.md |
| Complex | >10 | Create full Epic |

## Gotchas

- Claude Agent SDK must be installed: `pip install claude-agent-sdk`
- ANTHROPIC_API_KEY must be set in `.env`
- Each session creates a workspace in `AGENT_WORKSPACE_DIR`

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
