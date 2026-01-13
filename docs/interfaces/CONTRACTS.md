# Module Interface Contracts

## Overview

This document defines the public interfaces between modules. All cross-module communication MUST go through these defined contracts.

---

## Contract Principles

1. **Stability**: Once published, interfaces should not break backward compatibility
2. **Explicit**: All inputs and outputs must be typed
3. **Documented**: Each method must have clear documentation
4. **Versioned**: Breaking changes require version bump

---

## Module Contracts

### UserService (user module)

**Location**: `src/modules/user/interface.py`

```python
class IUserService(Protocol):
    """User management interface for other modules."""
    
    def get_user(self, user_id: str) -> User | None:
        """
        Retrieve user by ID.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            User object if found, None otherwise
        """
        ...
    
    def create_user(self, data: CreateUserDTO) -> User:
        """
        Create a new user.
        
        Args:
            data: User creation data
            
        Returns:
            Created user object
            
        Raises:
            UserExistsError: If email already registered
            ValidationError: If data is invalid
        """
        ...
```

**DTOs**:

```python
@dataclass
class CreateUserDTO:
    email: str
    name: str
    password: str

@dataclass  
class User:
    id: str
    email: str
    name: str
    created_at: datetime
```

---

### [ModuleName]Service ([module] module)

**Location**: `src/modules/[module]/interface.py`

```python
class I[ModuleName]Service(Protocol):
    """[Description of what this interface provides]."""
    
    def method_name(self, arg: ArgType) -> ReturnType:
        """
        [Method description].
        
        Args:
            arg: [Description]
            
        Returns:
            [Description]
            
        Raises:
            [Error]: [When]
        """
        ...
```

---

## Shared DTOs

DTOs that are used across multiple modules.

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
