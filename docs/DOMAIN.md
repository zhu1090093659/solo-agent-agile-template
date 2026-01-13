# Domain Knowledge & Glossary

> Merged from: DOMAIN.md, GLOSSARY.md

---

## Business Overview

### What We Do

This is an AI Agent template powered by Claude Code. It provides a full-stack solution for building custom AI assistants with:
- Web chat interface
- Claude Code CLI as the agent engine
- Session and workspace management

### Target Users

| User Type | Description | Primary Goals |
|-----------|-------------|---------------|
| Developers | Build custom AI agents | Create branded agent experiences |
| End Users | Chat with the agent | Get AI-powered assistance |

---

## Core Domain Concepts

### Session

**Definition**: A conversation context between a user and the agent.

**Properties**:
- `session_id`: Unique identifier (UUID)
- `message_count`: Number of messages exchanged
- `workspace`: Isolated directory for agent operations

**Lifecycle**:
```
Created -> Active -> Idle -> Cleanup
```

---

### Agent

**Definition**: The AI assistant powered by Claude Code CLI.

**Components**:
- System prompt (personality/instructions)
- Allowed tools (capabilities)
- Workspace (operating environment)

---

### Message

**Definition**: A single exchange in a conversation.

**Types**:
| Type | Direction | Description |
|------|-----------|-------------|
| User | User → Agent | User's input |
| Assistant | Agent → User | Agent's response |
| Tool Use | Agent internal | Tool execution request |
| Tool Result | Agent internal | Tool execution output |

---

### Workspace

**Definition**: An isolated directory where the agent can operate.

**Purpose**:
- Security isolation per session
- Persistent file operations within session
- Automatic cleanup on session end

---

## Glossary

### Core Terms

| Term | Definition | Usage Notes |
|------|------------|-------------|
| Agent | The AI assistant instance | Not "bot" or "chatbot" |
| Session | A conversation context | Not "chat" or "thread" |
| Workspace | Isolated agent directory | Not "sandbox" |
| Driver | Claude Code CLI wrapper | Internal component |
| Prompt | System instructions | Not "template" |

### Technical Terms

| Term | Definition | Context |
|------|------------|---------|
| SSE | Server-Sent Events | Streaming protocol |
| CLI | Command Line Interface | Claude Code execution |
| DTO | Data Transfer Object | API layer |

### Abbreviations

| Abbr | Full Form | Context |
|------|-----------|---------|
| API | Application Programming Interface | General |
| SSE | Server-Sent Events | Streaming |
| UUID | Universally Unique Identifier | IDs |
| CLI | Command Line Interface | Execution |

---

## Naming Conventions

### In Code

| Context | Convention | Example |
|---------|------------|---------|
| Class names | PascalCase | `AgentService` |
| Function names | snake_case | `get_session()` |
| Variables | snake_case | `session_id` |
| Constants | UPPER_SNAKE | `MAX_TURNS` |
| API endpoints | kebab-case | `/chat/message` |

### In Documentation

| Context | Convention | Example |
|---------|------------|---------|
| Referring to code | backticks | `AgentService` |
| File paths | backticks | `src/modules/agent/` |
| Concepts | normal text | agent service |

---

## Business Rules

### Session Rules

| Rule | Description |
|------|-------------|
| Isolation | Each session has its own workspace |
| Timeout | Sessions cleanup after inactivity |
| Continuation | Messages continue previous context |

### Tool Restrictions

| Context | Allowed Tools |
|---------|---------------|
| Default | All Claude Code tools |
| Restricted | Configurable subset |

---

## Status Values

### Session Status

| Status | Meaning |
|--------|---------|
| active | Currently in use |
| idle | Waiting for messages |
| ended | Cleaned up |

### Message Event Types

| Event | Meaning |
|-------|---------|
| text | Text content from agent |
| tool_use | Agent requesting tool execution |
| tool_result | Result of tool execution |
| error | Error occurred |
| done | Response complete |

---

## Confusing Terms Clarification

### Session vs Conversation

- **Session**: The technical container (workspace, ID, state)
- **Conversation**: The semantic content (messages, context)

A session contains one conversation.

### Agent vs Driver vs Service

- **Agent**: The conceptual AI assistant
- **Driver**: Low-level Claude Code CLI wrapper
- **Service**: High-level business logic layer

---

## Adding New Terms

When adding a new term:

1. Check if a similar term already exists
2. Define clearly with usage context
3. Add code examples if applicable
4. Update relevant documentation
