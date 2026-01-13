# Code Conventions

## General Principles

1. **Clarity over cleverness**: Code should be easy to read and understand
2. **Explicit over implicit**: Make intentions clear
3. **Consistency**: Follow established patterns in the codebase
4. **Small units**: Functions and classes should do one thing well

---

## Naming Conventions

### Files and Directories

| Type | Convention | Example |
|------|------------|---------|
| Python files | snake_case | `user_service.py` |
| TypeScript files | camelCase | `useChat.ts` |
| Test files | test_[name] | `test_service.py` |
| Directories | snake_case | `chat/` |

### Code Elements

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `AgentService` |
| Functions | snake_case (Python) | `get_session()` |
| Functions | camelCase (TS) | `sendMessage()` |
| Variables | snake_case / camelCase | `session_id` / `sessionId` |
| Constants | UPPER_SNAKE_CASE | `MAX_TURNS` |
| Private | Leading underscore | `_internal_method()` |

### API

| Type | Convention | Example |
|------|------------|---------|
| Endpoints | kebab-case | `/chat/message` |
| Query params | snake_case | `?session_id=...` |
| JSON fields | camelCase | `{"sessionId": "..."}` |

---

## Code Structure

### Python Module Layout

```
module/
    __init__.py          # Public exports
    service.py           # Main service class
    models.py            # Domain models
    schemas.py           # Input/output schemas
    exceptions.py        # Module-specific errors
```

### Function Structure

```python
def function_name(required_arg: Type, optional_arg: Type = default) -> ReturnType:
    """
    Brief description of what the function does.
    
    Args:
        required_arg: Description of this argument
        optional_arg: Description of this argument
        
    Returns:
        Description of return value
        
    Raises:
        ErrorType: When this error occurs
    """
    # Validate inputs first
    if not required_arg:
        raise ValueError("required_arg cannot be empty")
    
    # Main logic
    result = do_something(required_arg)
    
    return result
```

### Class Structure

```python
class ServiceName:
    """Brief description of the service."""
    
    def __init__(self, dependency: DependencyType) -> None:
        """Initialize with dependencies."""
        self._dependency = dependency
    
    # Public methods first
    def public_method(self) -> ReturnType:
        """Public method description."""
        return self._private_helper()
    
    # Private methods after
    def _private_helper(self) -> ReturnType:
        """Private helper description."""
        pass
```

---

## Import Order

```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party packages
import httpx
from pydantic import BaseModel

# 3. Local application
from modules.agent.service import agent_service
```

---

## Error Handling

### Do

```python
# Specific exception types
try:
    session = await service.get_session(session_id)
except NotFoundError:
    raise HTTPException(status_code=404, detail="Session not found")
except Exception as e:
    logger.error("Unexpected error", error=str(e))
    raise
```

### Do Not

```python
# Too broad - hides bugs
try:
    session = await service.get_session(session_id)
except Exception:
    pass  # Silent failure - NEVER do this
```

---

## Logging

### Format

```python
# Use structured logging
logger.info(
    "Chat completed",
    session_id=session.id,
    message_count=count,
)

# Not string formatting
logger.info(f"Chat {session_id} completed")  # Avoid
```

### Levels

| Level | Use For |
|-------|---------|
| DEBUG | Detailed diagnostic information |
| INFO | Routine operations, milestones |
| WARNING | Unexpected but handled situations |
| ERROR | Errors that need attention |

---

## Comments

### When to Comment

- Complex algorithms that need explanation
- Non-obvious business rules
- Workarounds with reference to issues
- TODO items with context

### Comment Format

```python
# Simple explanation
x = x + 1  # Increment counter

# TODO with context
# TODO: Refactor when Python 3.12 available
#       See: https://github.com/org/repo/issues/123
```

---

## Git Conventions

### Branch Naming

```
feature/[issue-id]-short-description
bugfix/[issue-id]-short-description
hotfix/critical-fix
```

### Commit Messages

```
type(scope): brief description

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(agent): add tool restriction support
fix(chat): handle SSE connection drops
docs(api): update endpoint examples
```
