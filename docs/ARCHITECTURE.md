# Architecture

> Merged from: OVERVIEW.md, MODULES.md, DATA_FLOW.md

---

## System Context

```mermaid
flowchart LR
    User([User]) --> Frontend[React Frontend]
    Frontend <--> Backend[FastAPI Backend]
    Backend <--> CC[Claude Code CLI]
    CC <--> Claude[Claude API]
    Backend <--> DB[(PostgreSQL)]
    
    style CC fill:#a855f7,color:#fff
```

## High-Level Architecture

```mermaid
flowchart TB
    subgraph Frontend["Frontend (React)"]
        UI[Chat Interface]
        Hook[useChat Hook]
        SSE[SSE Stream Handler]
    end
    
    subgraph Backend["Backend (FastAPI)"]
        API[Chat API Routes]
        Service[Agent Service]
        Driver[Claude Code Driver]
    end
    
    subgraph Engine["Agent Engine"]
        CLI[Claude Code CLI]
        Workspace[Session Workspace]
    end
    
    subgraph External["External"]
        Claude[Claude API]
    end
    
    UI --> Hook
    Hook --> SSE
    SSE <--> API
    API --> Service
    Service --> Driver
    Driver --> CLI
    CLI --> Workspace
    CLI <--> Claude
```

---

## Component Details

### Frontend Components

| Component | Location | Purpose |
|-----------|----------|---------|
| ChatWindow | `components/chat/ChatWindow.tsx` | Main chat container |
| ChatMessage | `components/chat/ChatMessage.tsx` | Message bubble |
| ChatInput | `components/chat/ChatInput.tsx` | Input field |
| useChat | `hooks/useChat.ts` | SSE streaming hook |

### Backend Modules

| Module | Location | Purpose |
|--------|----------|---------|
| Agent Driver | `modules/agent/driver.py` | Executes Claude Code CLI |
| Agent Service | `modules/agent/service.py` | Manages prompts & sessions |
| Chat Router | `modules/chat/router.py` | API endpoints |

---

## Module Architecture

### Module Dependency Graph

```mermaid
flowchart TB
    Core[core]
    Agent[agent]
    Chat[chat]
    API[api]
    
    Core --> Agent
    Core --> Chat
    Agent --> API
    Chat --> API
```

### Module Registry

| Module | Location | Responsibility | Status |
|--------|----------|----------------|--------|
| core | `src/modules/core` | Shared domain primitives | Stable |
| agent | `src/modules/agent` | Claude Code integration | Stable |
| chat | `src/modules/chat` | Chat API routes | Stable |

### Cross-Module Communication

**Allowed Patterns:**

1. **Direct Import** (within same layer):
   ```python
   from modules.agent.service import agent_service
   ```

2. **Interface/Protocol** (cross-layer):
   ```python
   from modules.agent.interface import IAgentService
   ```

**Forbidden Patterns:**
- Direct database access from presentation layer
- Circular dependencies between modules
- Importing internal implementation details

### Adding a New Module

1. Create directory: `src/modules/[name]/`
2. Add required files: `__init__.py`, `service.py`
3. Register in module registry above
4. Update dependency graph if needed

---

## Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant D as Driver
    participant C as Claude Code
    participant A as Claude API

    U->>F: Type message
    F->>B: POST /api/chat/message
    B->>D: execute(message, session_id)
    D->>C: claude --print "message"
    C->>A: API request
    A-->>C: Stream response
    C-->>D: JSON events
    D-->>B: Yield events
    B-->>F: SSE stream
    F-->>U: Display response
```

---

## Data Flow

### Message Format

```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolUse?: {
    tool: string;
    input: object;
    output?: string;
  }[];
}
```

### SSE Events

```
event: text
data: {"type": "text", "content": "Hello..."}

event: tool_use
data: {"type": "tool_use", "tool": "Bash", "input": {"command": "ls"}}

event: tool_result
data: {"type": "tool_result", "tool": "Bash", "output": "file1 file2"}

event: done
data: {"type": "done"}
```

### Data Transformation

```mermaid
flowchart TB
    Raw[Raw HTTP Request] --> Validation
    Validation -->|Invalid| Error[ValidationError]
    Validation -->|Valid| DTO[DTO/Schema]
    DTO --> Service[Service Layer]
    Service --> Response[HTTP Response]
```

---

## Session Management

```mermaid
flowchart TD
    A[New Message] --> B{Session Exists?}
    B -->|No| C[Create Session]
    C --> D[Create Workspace]
    D --> E[Execute Claude Code]
    B -->|Yes| E
    E --> F[Stream Response]
    F --> G{More Messages?}
    G -->|Yes| E
    G -->|No| H[Session Idle]
    H -->|Timeout| I[Cleanup Workspace]
```

---

## Security Considerations

### Workspace Isolation

Each session runs in an isolated directory:

```
/tmp/agent_workspaces/
├── session-uuid-1/
├── session-uuid-2/
└── session-uuid-3/
```

### Tool Restrictions

Control which Claude Code tools are available:

```python
allowed_tools = [
    "Read",      # Read files
    "Write",     # Write files
    "Bash",      # Run commands
    # Omit dangerous tools
]
```

### Timeouts

- Request timeout: 5 minutes default
- Max turns: 10 iterations
- Session cleanup: automatic on end

---

## Scaling Considerations

### Current Limits

- One Claude Code process per request
- Workspace disk usage per session
- API rate limits

### Future Scaling

- Session pooling
- Workspace caching
- Distributed execution

---

## Caching Strategy (if applicable)

```mermaid
flowchart LR
    Request([Request]) --> L1[L1 Local Cache]
    L1 -->|Miss| L2[L2 Redis]
    L2 -->|Miss| DB[(Database)]
    DB --> L2
    L2 --> L1
    L1 --> Response([Response])
```

| Pattern | TTL | Invalidation |
|---------|-----|--------------|
| `session:{id}` | 1h | On session end |
| `config:*` | 24h | Manual refresh |

---

## Error Handling Flow

```mermaid
flowchart TB
    Ex[Exception Raised] --> Handler[Exception Handler]
    Handler --> Log[Log Error]
    Handler --> Mapper[Error Mapper]
    Mapper --> Status[Map to HTTP Status]
    Status --> Response[Error Response]
    Response --> Client([Return to Client])
```

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```
