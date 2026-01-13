# Testing Standards

## Testing Philosophy

1. **Test behavior, not implementation**: Tests verify what code does, not how
2. **Fast feedback**: Unit tests should run in milliseconds
3. **Reliable**: No flaky tests, no external dependencies
4. **Readable**: Tests serve as documentation

---

## Test Pyramid

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
            agent/
                test_service.py
                test_driver.py
            chat/
                test_router.py
    integration/
        test_chat_flow.py
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
def test_chat_with_valid_message_returns_response():
    pass

def test_chat_with_empty_message_raises_error():
    pass
```

---

## Test Structure (AAA Pattern)

```python
def test_session_creation():
    # Arrange - Set up test data
    service = AgentService()
    session_id = "test-123"
    
    # Act - Execute the behavior
    session = service.start_session(session_id)
    
    # Assert - Verify the results
    assert session["id"] == session_id
    assert session["message_count"] == 0
```

---

## Fixtures

### Basic Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def agent_service():
    return AgentService()

@pytest.fixture
def mock_driver():
    return AsyncMock(spec=ClaudeSDKDriver)
```

### Factory Fixtures

```python
@pytest.fixture
def session_factory():
    def _create_session(**overrides):
        defaults = {
            "id": str(uuid4()),
            "message_count": 0,
        }
        return {**defaults, **overrides}
    return _create_session
```

---

## Mocking Guidelines

### When to Mock

- External services (Claude Agent SDK)
- Time-dependent code
- Slow operations

### When NOT to Mock

- The code under test
- Simple data objects
- In integration tests

### Mock Examples

```python
from unittest.mock import Mock, AsyncMock, patch

# Async mock for driver
async def test_chat_streams_response(mock_driver):
    mock_driver.execute = AsyncMock(return_value=async_gen([
        {"type": "text", "content": "Hello"},
        {"type": "done"}
    ]))
    
    service = AgentService(mock_driver)
    events = [e async for e in service.chat("Hi", "session-1")]
    
    assert len(events) == 2
    assert events[0]["type"] == "text"
```

---

## Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_async_chat():
    service = AgentService()
    events = []
    
    async for event in service.chat("Hello", "session-1"):
        events.append(event)
    
    assert len(events) > 0
```

---

## Integration Tests

```python
@pytest.mark.integration
async def test_full_chat_flow(test_client):
    """Test complete chat flow through API."""
    # Create session
    response = await test_client.post("/api/chat/sessions")
    session_id = response.json()["session_id"]
    
    # Send message
    response = await test_client.post(
        "/api/chat/message",
        json={"message": "Hello", "session_id": session_id}
    )
    
    assert response.status_code == 200
```

---

## Assertions

### Preferred

```python
# Clear assertions
assert session.id == "expected-id"
assert len(events) == 3
assert "error" not in response.json()

# For exceptions
with pytest.raises(SessionNotFoundError):
    service.get_session("nonexistent")
```

### Avoid

```python
# Too vague
assert result  # What should result be?

# Testing implementation details
mock.method.assert_called_with(...)  # Usually unnecessary
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/modules/agent/test_service.py

# Run by marker
pytest -m integration

# Stop on first failure
pytest -x

# Verbose output
pytest -v
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
