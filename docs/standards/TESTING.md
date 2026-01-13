# Testing Standards

## Testing Philosophy

1. **Test behavior, not implementation**: Tests should verify what code does, not how
2. **Fast feedback**: Unit tests should run in milliseconds
3. **Reliable**: No flaky tests, no external dependencies
4. **Readable**: Tests serve as documentation

---

## Test Pyramid

```mermaid
%%{init: {'theme': 'default'}}%%
graph TB
    subgraph Pyramid["Test Pyramid"]
        E2E["E2E Tests<br/>(few, slow)"]
        INT["Integration Tests<br/>(some)"]
        UNIT["Unit Tests<br/>(many, fast)"]
    end
    
    E2E --- INT
    INT --- UNIT
    
    style E2E fill:#ff6b6b,color:#fff
    style INT fill:#ffd93d,color:#000
    style UNIT fill:#6bcb77,color:#fff
```

| Type | Count | Speed | Scope |
|------|-------|-------|-------|
| Unit | Many | Fast (<100ms) | Single function/class |
| Integration | Some | Medium (<5s) | Module boundaries |
| E2E | Few | Slow (<30s) | Full user flows |

---

## Directory Structure

```
tests/
    conftest.py              # Shared fixtures
    unit/
        modules/
            user/
                test_service.py
                test_repository.py
            order/
                test_service.py
    integration/
        test_user_order_flow.py
        test_api_endpoints.py
    e2e/
        test_checkout_flow.py
    fixtures/
        users.py
        orders.py
```

---

## Naming Conventions

### Test Files

```
test_[module_name].py
```

### Test Functions

```python
def test_[what]_[condition]_[expected_result]():
    pass

# Examples
def test_create_user_with_valid_email_returns_user():
    pass

def test_create_user_with_duplicate_email_raises_conflict_error():
    pass

def test_get_user_when_not_found_returns_none():
    pass
```

### Test Classes (for grouping)

```python
class TestUserCreation:
    def test_with_valid_data_succeeds(self):
        pass
    
    def test_with_invalid_email_fails(self):
        pass
```

---

## Test Structure (AAA Pattern)

```python
def test_order_total_calculation():
    # Arrange - Set up test data and conditions
    items = [
        OrderItem(price=10.00, quantity=2),
        OrderItem(price=5.00, quantity=3),
    ]
    order = Order(items=items)
    
    # Act - Execute the behavior being tested
    total = order.calculate_total()
    
    # Assert - Verify the results
    assert total == 35.00
```

---

## Fixtures

### Basic Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def sample_user():
    return User(
        id="user-123",
        email="test@example.com",
        name="Test User"
    )

@pytest.fixture
def sample_order(sample_user):
    return Order(
        id="order-123",
        user_id=sample_user.id,
        items=[]
    )
```

### Factory Fixtures

```python
@pytest.fixture
def user_factory():
    def _create_user(**overrides):
        defaults = {
            "id": str(uuid4()),
            "email": f"user-{uuid4()}@example.com",
            "name": "Test User",
        }
        return User(**{**defaults, **overrides})
    return _create_user

# Usage
def test_something(user_factory):
    user1 = user_factory(name="Alice")
    user2 = user_factory(name="Bob")
```

### Database Fixtures

```python
@pytest.fixture
async def db_session():
    """Create a test database session with rollback."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()
```

---

## Mocking Guidelines

### When to Mock

- External services (APIs, databases in unit tests)
- Time-dependent code
- Random/non-deterministic code
- Slow operations

### When NOT to Mock

- The code under test
- Simple data objects
- In integration tests (use real implementations)

### Mock Examples

```python
from unittest.mock import Mock, AsyncMock, patch

# Simple mock
def test_with_mock():
    mock_repo = Mock(spec=UserRepository)
    mock_repo.get.return_value = User(id="123", email="test@example.com")
    
    service = UserService(mock_repo)
    user = service.get_user("123")
    
    assert user.email == "test@example.com"

# Async mock
async def test_with_async_mock():
    mock_repo = AsyncMock(spec=UserRepository)
    mock_repo.get.return_value = User(id="123")
    
    service = UserService(mock_repo)
    user = await service.get_user("123")

# Patch decorator
@patch("modules.user.service.send_email")
def test_user_creation_sends_email(mock_send_email):
    service = UserService()
    service.create_user(data)
    
    mock_send_email.assert_called_once_with(data.email)
```

---

## Assertions

### Preferred Assertions

```python
# Use plain assert with clear conditions
assert user.email == "test@example.com"
assert len(orders) == 3
assert "error" in response.json()

# For exceptions
with pytest.raises(UserNotFoundError) as exc_info:
    service.get_user("nonexistent")
assert "nonexistent" in str(exc_info.value)

# For approximate values
assert total == pytest.approx(10.5, rel=0.01)
```

### Avoid

```python
# Too vague
assert result  # What should result be?

# Testing implementation
mock.method.assert_called_with(...)  # Usually unnecessary
```

---

## Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result == expected

# With fixtures
@pytest.fixture
async def async_client():
    async with AsyncClient(app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_api_endpoint(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200
```

---

## Integration Tests

```python
@pytest.mark.integration
async def test_user_order_flow(db_session, event_bus):
    """Test complete flow: user creates order, payment processed."""
    # Create user
    user_service = UserService(UserRepository(db_session))
    user = await user_service.create_user(CreateUserDTO(...))
    
    # Create order
    order_service = OrderService(
        OrderRepository(db_session),
        user_service,
        event_bus
    )
    order = await order_service.create_order(user.id, items)
    
    # Verify
    assert order.status == OrderStatus.PENDING
    assert len(event_bus.published) == 1
    assert event_bus.published[0].type == "order.created"
```

---

## Test Data Management

### In-Memory Repositories

```python
class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users: dict[str, User] = {}
    
    async def get(self, user_id: str) -> User | None:
        return self._users.get(user_id)
    
    async def save(self, user: User) -> None:
        self._users[user.id] = user
```

### Test Database

```python
# Use separate test database
TEST_DATABASE_URL = "postgresql://test:test@localhost/test_db"

@pytest.fixture(scope="session")
def test_db():
    # Create test database
    create_database(TEST_DATABASE_URL)
    yield
    # Cleanup
    drop_database(TEST_DATABASE_URL)
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/modules/user/test_service.py

# Run specific test
pytest tests/unit/modules/user/test_service.py::test_create_user

# Run by marker
pytest -m integration
pytest -m "not slow"

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x
```

---

## Coverage Requirements

| Type | Minimum Coverage |
|------|------------------|
| Overall | 80% |
| Critical paths | 95% |
| New code | 90% |

```bash
# Check coverage
pytest --cov=src --cov-fail-under=80
```

---

## CI Integration

```yaml
# .github/workflows/test.yml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```
