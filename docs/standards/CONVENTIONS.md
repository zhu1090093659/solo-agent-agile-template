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
| TypeScript files | camelCase or kebab-case | `userService.ts` or `user-service.ts` |
| Test files | [name]_test or [name].test | `user_service_test.py` |
| Directories | snake_case | `user_management/` |

### Code Elements

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `UserService` |
| Functions | snake_case (Python) / camelCase (TS) | `get_user()` / `getUser()` |
| Variables | snake_case (Python) / camelCase (TS) | `user_name` / `userName` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Private | Leading underscore | `_internal_method()` |

### Database

| Type | Convention | Example |
|------|------------|---------|
| Tables | snake_case, plural | `user_accounts` |
| Columns | snake_case | `created_at` |
| Indexes | `idx_[table]_[columns]` | `idx_users_email` |
| Foreign keys | `fk_[table]_[ref_table]` | `fk_orders_users` |

### API

| Type | Convention | Example |
|------|------------|---------|
| Endpoints | kebab-case, plural | `/user-accounts` |
| Query params | snake_case | `?page_size=20` |
| JSON fields | camelCase | `{"userName": "..."}` |

---

## Code Structure

### Python Module Layout

```
module/
    __init__.py          # Public exports
    service.py           # Main service class
    models.py            # Domain models
    repository.py        # Data access
    schemas.py           # Input/output schemas
    exceptions.py        # Module-specific errors
    constants.py         # Module constants
    utils.py             # Helper functions
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
    
    # Return
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
from modules.core import exceptions
from modules.user.service import UserService
```

---

## Error Handling

### Do

```python
# Specific exception types
try:
    user = await repository.get(user_id)
except NotFoundError:
    raise UserNotFoundError(user_id)
except DatabaseError as e:
    logger.error("Database error", error=e, user_id=user_id)
    raise
```

### Do Not

```python
# Too broad
try:
    user = await repository.get(user_id)
except Exception:
    pass  # Silent failure

# Catching and re-raising same exception
try:
    something()
except ValueError:
    raise ValueError  # Loses stack trace
```

---

## Logging

### Format

```python
# Use structured logging
logger.info(
    "User created",
    user_id=user.id,
    email=user.email,
    source="api"
)

# Not string formatting
logger.info(f"User {user.id} created")  # Avoid
```

### Levels

| Level | Use For |
|-------|---------|
| DEBUG | Detailed diagnostic information |
| INFO | Routine operations, milestones |
| WARNING | Unexpected but handled situations |
| ERROR | Errors that need attention |
| CRITICAL | System failures |

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
# TODO(username): Refactor when Python 3.12 is available
#                 See: https://github.com/org/repo/issues/123

# Complex logic explanation
# We use binary search here because the list is sorted and
# can contain millions of items. Linear search was too slow
# (see ADR-005 for benchmarks).
```

---

## Testing Conventions

### Test File Location

```
src/
    modules/
        user/
            service.py
tests/
    modules/
        user/
            test_service.py
```

### Test Function Naming

```python
def test_[what]_[condition]_[expected]():
    """Test description."""
    pass

# Examples
def test_create_user_with_valid_data_returns_user():
    pass

def test_create_user_with_duplicate_email_raises_conflict():
    pass
```

### Test Structure (AAA)

```python
def test_something():
    # Arrange
    user = create_test_user()
    
    # Act
    result = service.do_something(user)
    
    # Assert
    assert result.status == "completed"
```

---

## Git Conventions

### Branch Naming

```
feature/[issue-id]-short-description
bugfix/[issue-id]-short-description
hotfix/[issue-id]-short-description
refactor/short-description
```

### Commit Messages

```
type(scope): brief description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(user): add email verification flow
fix(auth): handle expired token gracefully
docs(api): update authentication examples
```
