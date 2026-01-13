# Internal Interfaces

> Merged from: CONTRACTS.md, EVENTS.md

---

## Overview

This document defines:
1. **Module Contracts** - Public interfaces between modules
2. **Event Definitions** - Async communication between modules

All cross-module communication MUST go through these defined contracts.

---

# Part 1: Module Contracts

## Contract Principles

1. **Stability**: Once published, interfaces should not break backward compatibility
2. **Explicit**: All inputs and outputs must be typed
3. **Documented**: Each method must have clear documentation
4. **Versioned**: Breaking changes require version bump

---

## Agent Service Contract

**Location**: `src/modules/agent/service.py`

```python
class AgentService:
    """Agent service interface for chat module."""
    
    async def chat(
        self,
        message: str,
        session_id: str,
        continue_conversation: bool = True
    ) -> AsyncIterator[dict]:
        """
        Send a message and stream response.
        
        Args:
            message: User message
            session_id: Session ID
            continue_conversation: Whether to continue previous context
            
        Yields:
            Event dicts: text, tool_use, tool_result, error, done
        """
        ...
    
    async def chat_simple(self, message: str, session_id: str) -> str:
        """
        Send message and get complete response.
        
        Non-streaming convenience method.
        """
        ...
    
    def start_session(self, session_id: str) -> dict:
        """Start a new chat session."""
        ...
    
    def end_session(self, session_id: str) -> None:
        """End and cleanup a session."""
        ...
```

---

## Shared DTOs

DTOs used across multiple modules.

**Location**: `src/modules/core/dto.py`

```python
@dataclass
class PaginationParams:
    page: int = 1
    per_page: int = 20
    
@dataclass
class PaginatedResult(Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int
    has_next: bool
```

---

## Error Contracts

**Location**: `src/modules/core/errors.py`

| Error Class | HTTP Status | When to Use |
|-------------|-------------|-------------|
| `NotFoundError` | 404 | Resource not found |
| `ValidationError` | 400 | Invalid input data |
| `AuthenticationError` | 401 | Not authenticated |
| `AuthorizationError` | 403 | Not authorized |
| `ConflictError` | 409 | Resource conflict |

---

## Versioning Strategy

When making breaking changes:

1. Create new interface version: `IUserServiceV2`
2. Keep old interface working
3. Add deprecation notice
4. Remove old interface after migration period

```python
# Deprecated - use IUserServiceV2
@deprecated("Use IUserServiceV2 instead, removal in v2.0")
class IUserService(Protocol):
    ...

class IUserServiceV2(Protocol):
    ...
```

---

# Part 2: Event Definitions

## Event Naming Convention

```
[domain].[entity].[action]

Examples:
- session.chat.started
- session.chat.completed
- agent.tool.executed
```

---

## Event Registry

### Session Domain

#### session.chat.started

**Trigger**: New chat message received
**Producer**: ChatRouter
**Payload**:

```python
{
    "event_type": "session.chat.started",
    "timestamp": "2024-01-01T00:00:00Z",
    "data": {
        "session_id": "uuid",
        "message": "user message"
    }
}
```

---

#### session.chat.completed

**Trigger**: Chat response fully delivered
**Producer**: AgentService
**Payload**:

```python
{
    "event_type": "session.chat.completed",
    "timestamp": "2024-01-01T00:00:00Z",
    "data": {
        "session_id": "uuid",
        "response_length": 1234,
        "tool_calls": 3
    }
}
```

---

### Agent Domain

#### agent.tool.executed

**Trigger**: Claude SDK tool execution
**Producer**: ClaudeSDKDriver
**Payload**:

```python
{
    "event_type": "agent.tool.executed",
    "timestamp": "2024-01-01T00:00:00Z",
    "data": {
        "session_id": "uuid",
        "tool": "Bash",
        "input": {"command": "ls"},
        "success": true
    }
}
```

---

## Event Infrastructure

### Publishing Events

```python
from core.events import event_bus

# Publish an event
await event_bus.publish(
    "session.chat.completed",
    session_id=session.id,
    response_length=len(response)
)
```

### Subscribing to Events

```python
from core.events import event_bus

@event_bus.subscribe("session.chat.completed")
async def handle_chat_completed(event: Event):
    session_id = event.data["session_id"]
    # Handle event
```

---

## Event Guarantees

| Property | Guarantee |
|----------|-----------|
| Delivery | At least once |
| Ordering | Per-session ordered |
| Retention | In-memory (no persistence) |

---

## Error Handling

Failed event handlers:
1. Log error with full context
2. Continue processing (don't block main flow)
3. Optionally retry with backoff

---

## Adding New Interfaces

### New Contract

1. Define interface in module's `interface.py`
2. Document in this file
3. Add type hints and docstrings
4. Consider versioning strategy

### New Event

1. Define event type following naming convention
2. Document in this file
3. Create payload schema
4. Register producers and consumers
