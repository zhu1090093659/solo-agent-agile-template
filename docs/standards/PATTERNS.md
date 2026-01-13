# Recommended Patterns

## Overview

This document describes the design patterns and best practices used in this project.

---

## Dependency Injection

### Pattern

```python
# Define interface
class IUserRepository(Protocol):
    async def get(self, user_id: str) -> User | None: ...
    async def save(self, user: User) -> None: ...

# Service depends on interface, not implementation
class UserService:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository
    
    async def get_user(self, user_id: str) -> User:
        user = await self._repository.get(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

# Wire up in composition root
def create_user_service() -> UserService:
    repository = PostgresUserRepository(db_session)
    return UserService(repository)
```

### Benefits

- Testable (inject mocks)
- Flexible (swap implementations)
- Clear dependencies

---

## Repository Pattern

### Pattern

```python
class UserRepository:
    """Data access for User entity."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get(self, user_id: str) -> User | None:
        """Get user by ID."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        row = result.scalar_one_or_none()
        return User.from_orm(row) if row else None
    
    async def save(self, user: User) -> None:
        """Save user (insert or update)."""
        model = UserModel(**user.dict())
        self._session.add(model)
        await self._session.flush()
    
    async def find_by_email(self, email: str) -> User | None:
        """Find user by email."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        row = result.scalar_one_or_none()
        return User.from_orm(row) if row else None
```

### Guidelines

- One repository per aggregate root
- Repository returns domain objects, not ORM models
- Keep queries in repository, not service

---

## Service Layer Pattern

### Pattern

```python
class OrderService:
    """Business logic for order operations."""
    
    def __init__(
        self,
        order_repo: IOrderRepository,
        user_repo: IUserRepository,
        payment_service: IPaymentService,
        event_bus: IEventBus,
    ) -> None:
        self._orders = order_repo
        self._users = user_repo
        self._payments = payment_service
        self._events = event_bus
    
    async def create_order(self, user_id: str, items: list[OrderItem]) -> Order:
        """Create a new order for user."""
        # Validate user exists
        user = await self._users.get(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        
        # Create order
        order = Order.create(user_id=user_id, items=items)
        
        # Save
        await self._orders.save(order)
        
        # Publish event
        await self._events.publish("order.created", order_id=order.id)
        
        return order
```

### Guidelines

- Services contain business logic
- Services coordinate between repositories and external services
- One public method = one use case

---

## Result Pattern (for error handling)

### Pattern

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass  
class Err(Generic[E]):
    error: E

Result = Ok[T] | Err[E]

# Usage
def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

# Handling
result = divide(10, 2)
match result:
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")
```

### When to Use

- When failure is expected and not exceptional
- When you need to preserve error information
- In functional-style code

---

## Factory Pattern

### Pattern

```python
class NotificationFactory:
    """Create appropriate notification sender."""
    
    _senders: dict[str, type[INotificationSender]] = {
        "email": EmailSender,
        "sms": SmsSender,
        "push": PushSender,
    }
    
    @classmethod
    def create(cls, channel: str, config: Config) -> INotificationSender:
        sender_class = cls._senders.get(channel)
        if not sender_class:
            raise ValueError(f"Unknown channel: {channel}")
        return sender_class(config)
```

### When to Use

- Multiple implementations of same interface
- Complex object construction
- Decoupling creation from usage

---

## Decorator Pattern (for cross-cutting concerns)

### Pattern

```python
import functools
import time
from typing import Callable, TypeVar

T = TypeVar("T")

def with_retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator

# Usage
@with_retry(max_attempts=3)
async def call_external_api():
    ...
```

### Common Decorators

- `@with_retry` - Retry on failure
- `@with_timeout` - Add timeout
- `@with_cache` - Cache results
- `@with_logging` - Log calls

---

## Builder Pattern (for complex objects)

### Pattern

```python
class QueryBuilder:
    """Build complex database queries."""
    
    def __init__(self) -> None:
        self._filters: list[str] = []
        self._order_by: str | None = None
        self._limit: int | None = None
    
    def where(self, condition: str) -> "QueryBuilder":
        self._filters.append(condition)
        return self
    
    def order_by(self, field: str, desc: bool = False) -> "QueryBuilder":
        self._order_by = f"{field} {'DESC' if desc else 'ASC'}"
        return self
    
    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self
    
    def build(self) -> str:
        query = "SELECT * FROM table"
        if self._filters:
            query += " WHERE " + " AND ".join(self._filters)
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

# Usage
query = (
    QueryBuilder()
    .where("status = 'active'")
    .where("created_at > '2024-01-01'")
    .order_by("created_at", desc=True)
    .limit(10)
    .build()
)
```

---

## Strategy Pattern

### Pattern

```python
class PricingStrategy(Protocol):
    """Calculate price based on strategy."""
    def calculate(self, base_price: float, quantity: int) -> float: ...

class RegularPricing:
    def calculate(self, base_price: float, quantity: int) -> float:
        return base_price * quantity

class BulkPricing:
    def __init__(self, discount_threshold: int, discount_percent: float):
        self._threshold = discount_threshold
        self._discount = discount_percent
    
    def calculate(self, base_price: float, quantity: int) -> float:
        total = base_price * quantity
        if quantity >= self._threshold:
            total *= (1 - self._discount)
        return total

# Usage
class OrderCalculator:
    def __init__(self, pricing: PricingStrategy):
        self._pricing = pricing
    
    def calculate_total(self, items: list[Item]) -> float:
        return sum(
            self._pricing.calculate(item.price, item.quantity)
            for item in items
        )
```

---

## When to Apply Patterns

| Situation | Pattern |
|-----------|---------|
| Hide implementation details | Repository |
| Coordinate multiple operations | Service Layer |
| Need testable code | Dependency Injection |
| Multiple similar implementations | Strategy |
| Complex object creation | Factory / Builder |
| Cross-cutting concerns | Decorator |
| Expected failures | Result |
