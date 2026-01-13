# Anti-Patterns - Do Not Do These

## Overview

This document lists patterns and practices that are explicitly forbidden in this project, with explanations of why they are problematic.

---

## Code Level Anti-Patterns

### 1. Direct Database Access from API Layer

**Bad**:
```python
@router.get("/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

**Good**:
```python
@router.get("/users/{user_id}")
async def get_user(user_id: str, service: UserService = Depends()):
    return await service.get_user(user_id)
```

**Why**: Breaks separation of concerns, makes testing harder, scatters business logic.

---

### 2. Catching and Ignoring Exceptions

**Bad**:
```python
try:
    result = some_operation()
except Exception:
    pass  # Silent failure
```

**Good**:
```python
try:
    result = some_operation()
except SpecificError as e:
    logger.error("Operation failed", error=str(e))
    raise OperationFailedError(original=e)
```

**Why**: Hides bugs, makes debugging impossible, can lead to data corruption.

---

### 3. Hardcoded Configuration

**Bad**:
```python
def send_email():
    smtp_host = "smtp.gmail.com"
    api_key = "sk-12345"
```

**Good**:
```python
def send_email(config: EmailConfig):
    smtp_host = config.smtp_host
    api_key = config.api_key
```

**Why**: Security risk, impossible to deploy to different environments.

---

### 4. God Objects / God Functions

**Bad**:
```python
class UserManager:
    def create_user(self): ...
    def send_email(self): ...
    def process_payment(self): ...
    def generate_report(self): ...
    def validate_data(self): ...
    # 50 more methods
```

**Good**:
```python
class UserService:
    def create_user(self): ...

class EmailService:
    def send_email(self): ...

class PaymentService:
    def process_payment(self): ...
```

**Why**: Violates single responsibility, hard to test, hard to maintain.

---

### 5. Magic Numbers and Strings

**Bad**:
```python
if status == 1:
    discount = price * 0.15
    if days > 30:
        ...
```

**Good**:
```python
STATUS_ACTIVE = 1
DISCOUNT_RATE = 0.15
MAX_TRIAL_DAYS = 30

if status == STATUS_ACTIVE:
    discount = price * DISCOUNT_RATE
    if days > MAX_TRIAL_DAYS:
        ...
```

**Why**: Unclear meaning, hard to maintain, easy to make mistakes.

---

### 6. Mutable Default Arguments

**Bad**:
```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

**Good**:
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**Why**: Default mutable objects are shared across calls, causing bugs.

---

### 7. Nested Callbacks / Callback Hell

**Bad**:
```python
def process():
    fetch_user(lambda user:
        fetch_orders(user, lambda orders:
            fetch_items(orders, lambda items:
                process_items(items, lambda result:
                    save_result(result)
                )
            )
        )
    )
```

**Good**:
```python
async def process():
    user = await fetch_user()
    orders = await fetch_orders(user)
    items = await fetch_items(orders)
    result = await process_items(items)
    await save_result(result)
```

**Why**: Unreadable, hard to debug, hard to handle errors.

---

## Architecture Anti-Patterns

### 1. Circular Dependencies Between Modules

**Bad**:
```
user/ imports from order/
order/ imports from user/
```

**Good**:
```
core/ (shared interfaces)
user/ imports from core/
order/ imports from core/
```

**Why**: Creates tight coupling, makes testing hard, can cause import errors.

---

### 2. Cross-Module Direct Database Access

**Bad**:
```python
# In order module
from modules.user.models import UserModel

def get_order_with_user(order_id):
    order = session.query(OrderModel).get(order_id)
    user = session.query(UserModel).get(order.user_id)  # BAD
    return order, user
```

**Good**:
```python
# In order module
from modules.user.interface import IUserService

def get_order_with_user(order_id, user_service: IUserService):
    order = session.query(OrderModel).get(order_id)
    user = user_service.get_user(order.user_id)  # GOOD
    return order, user
```

**Why**: Bypasses business logic, creates hidden coupling.

---

### 3. Shared Mutable Global State

**Bad**:
```python
# globals.py
current_user = None
db_connection = None

# somewhere.py
import globals
globals.current_user = user
```

**Good**:
```python
# Use dependency injection
def process_request(user: User, db: Session):
    ...
```

**Why**: Race conditions, testing nightmare, implicit dependencies.

---

### 4. Sync External Calls in Request Path

**Bad**:
```python
@router.post("/orders")
async def create_order(order: OrderCreate):
    order = create_order(order)
    send_email_sync(order.user.email)  # Blocks request
    call_external_api_sync(order)       # Blocks request
    return order
```

**Good**:
```python
@router.post("/orders")
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    order = create_order(order)
    background_tasks.add_task(send_email, order.user.email)
    await event_bus.publish("order.created", order_id=order.id)
    return order
```

**Why**: Slow response times, poor user experience, cascade failures.

---

### 5. Leaky Abstractions

**Bad**:
```python
# Exposing ORM details through API
@router.get("/users")
async def list_users():
    return db.query(UserModel).all()  # Returns ORM objects
```

**Good**:
```python
@router.get("/users")
async def list_users(service: UserService = Depends()):
    users = await service.list_users()
    return [UserResponse.from_domain(u) for u in users]
```

**Why**: Tight coupling to implementation, security risks.

---

## Data Anti-Patterns

### 1. Storing Derived Data Without Update Strategy

**Bad**:
```python
class Order:
    items: list[Item]
    total: float  # Calculated once, never updated
```

**Good**:
```python
class Order:
    items: list[Item]
    
    @property
    def total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)
```

**Why**: Data gets out of sync, leads to bugs.

---

### 2. N+1 Query Problem

**Bad**:
```python
orders = db.query(Order).all()
for order in orders:
    user = db.query(User).get(order.user_id)  # N queries!
```

**Good**:
```python
orders = (
    db.query(Order)
    .options(joinedload(Order.user))
    .all()
)  # 1 query
```

**Why**: Severe performance degradation.

---

### 3. Unbounded Queries

**Bad**:
```python
def get_all_users():
    return db.query(User).all()  # Could be millions
```

**Good**:
```python
def get_users(page: int = 1, per_page: int = 20):
    return (
        db.query(User)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
```

**Why**: Memory issues, slow responses, potential crashes.

---

## Testing Anti-Patterns

### 1. Testing Implementation Instead of Behavior

**Bad**:
```python
def test_user_service():
    service = UserService(mock_repo)
    service.create_user(data)
    mock_repo.save.assert_called_once()  # Testing implementation
```

**Good**:
```python
def test_user_service():
    service = UserService(in_memory_repo)
    user = service.create_user(data)
    assert user.email == data.email  # Testing behavior
    assert in_memory_repo.get(user.id) is not None
```

**Why**: Brittle tests that break on refactoring.

---

### 2. Tests With External Dependencies

**Bad**:
```python
def test_payment():
    result = stripe.charge(card)  # Calls real Stripe!
    assert result.success
```

**Good**:
```python
def test_payment(mock_stripe):
    mock_stripe.charge.return_value = SuccessResult()
    result = payment_service.charge(card)
    assert result.success
```

**Why**: Flaky tests, costs money, requires network.

---

## Summary Checklist

Before submitting code, verify:

- [ ] No direct DB access from API layer
- [ ] No swallowed exceptions
- [ ] No hardcoded secrets or config
- [ ] No circular dependencies
- [ ] No sync external calls in request path
- [ ] No unbounded queries
- [ ] No N+1 queries
- [ ] No mutable default arguments
- [ ] No tests hitting external services
