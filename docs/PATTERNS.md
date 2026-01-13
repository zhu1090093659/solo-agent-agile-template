# Design Patterns & Anti-Patterns

> Merged from: PATTERNS.md, ANTI_PATTERNS.md

---

# Part 1: Recommended Patterns

## Dependency Injection

### Pattern

```python
# Service depends on interface, not implementation
class AgentService:
    def __init__(self, driver: ClaudeCodeDriver) -> None:
        self._driver = driver
    
    async def chat(self, message: str, session_id: str):
        async for event in self._driver.execute(message, session_id):
            yield event

# Wire up in composition root
def create_agent_service() -> AgentService:
    driver = ClaudeCodeDriver()
    return AgentService(driver)
```

### Benefits

- Testable (inject mocks)
- Flexible (swap implementations)
- Clear dependencies

---

## Service Layer Pattern

### Pattern

```python
class AgentService:
    """Business logic for agent operations."""
    
    def __init__(self, driver: ClaudeCodeDriver) -> None:
        self._driver = driver
        self._sessions: dict[str, dict] = {}
    
    async def chat(self, message: str, session_id: str) -> AsyncIterator[dict]:
        """Send a message and stream response."""
        # Ensure session exists
        if session_id not in self._sessions:
            self.start_session(session_id)
        
        # Execute through driver
        async for event in self._driver.execute(message, session_id):
            yield event
```

### Guidelines

- Services contain business logic
- Services coordinate between components
- One public method = one use case

---

## Factory Pattern

### Pattern

```python
class DriverFactory:
    """Create appropriate driver based on config."""
    
    @classmethod
    def create(cls, driver_type: str) -> IDriver:
        if driver_type == "claude_code":
            return ClaudeCodeDriver()
        elif driver_type == "mock":
            return MockDriver()
        raise ValueError(f"Unknown driver: {driver_type}")
```

### When to Use

- Multiple implementations of same interface
- Complex object construction
- Decoupling creation from usage

---

## Decorator Pattern (Cross-Cutting Concerns)

### Pattern

```python
def with_retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
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

---

## When to Apply Patterns

| Situation | Pattern |
|-----------|---------|
| Hide implementation details | Service Layer |
| Need testable code | Dependency Injection |
| Multiple implementations | Factory |
| Cross-cutting concerns | Decorator |

---

# Part 2: Anti-Patterns (DO NOT DO)

## Direct External Access from API Layer

**Bad**:
```python
@router.post("/chat")
async def chat(request: ChatRequest):
    # Directly calling driver from route - BAD
    driver = ClaudeCodeDriver()
    return await driver.execute(request.message)
```

**Good**:
```python
@router.post("/chat")
async def chat(request: ChatRequest, service: AgentService = Depends()):
    return await service.chat(request.message)
```

**Why**: Breaks separation of concerns, makes testing harder.

---

## Catching and Ignoring Exceptions

**Bad**:
```python
try:
    result = some_operation()
except Exception:
    pass  # Silent failure - NEVER
```

**Good**:
```python
try:
    result = some_operation()
except SpecificError as e:
    logger.error("Operation failed", error=str(e))
    raise OperationFailedError(original=e)
```

**Why**: Hides bugs, makes debugging impossible.

---

## Hardcoded Configuration

**Bad**:
```python
def create_driver():
    api_key = "sk-12345"  # Hardcoded - BAD
    timeout = 300
```

**Good**:
```python
def create_driver(config: Settings):
    api_key = config.ANTHROPIC_API_KEY
    timeout = config.AGENT_TIMEOUT
```

**Why**: Security risk, impossible to deploy to different environments.

---

## God Objects

**Bad**:
```python
class AgentManager:
    def chat(self): ...
    def send_email(self): ...
    def process_payment(self): ...
    def generate_report(self): ...
    # 50 more methods
```

**Good**:
```python
class AgentService:
    def chat(self): ...

class EmailService:
    def send_email(self): ...
```

**Why**: Violates single responsibility, hard to test and maintain.

---

## Magic Numbers and Strings

**Bad**:
```python
if turns > 10:
    raise TooManyTurnsError()
```

**Good**:
```python
MAX_TURNS = 10

if turns > MAX_TURNS:
    raise TooManyTurnsError()
```

**Why**: Unclear meaning, hard to maintain.

---

## Shared Mutable Global State

**Bad**:
```python
# globals.py
current_session = None

# somewhere.py
import globals
globals.current_session = session
```

**Good**:
```python
# Use dependency injection
def process_request(session: Session):
    ...
```

**Why**: Race conditions, testing nightmare.

---

## Sync Calls in Async Request Path

**Bad**:
```python
@router.post("/chat")
async def chat(request: ChatRequest):
    response = await agent.chat(request.message)
    send_email_sync(user.email)  # Blocks! BAD
    return response
```

**Good**:
```python
@router.post("/chat")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    response = await agent.chat(request.message)
    background_tasks.add_task(send_email, user.email)
    return response
```

**Why**: Slow response times, poor user experience.

---

## Summary Checklist

Before submitting code, verify:

- [ ] No direct driver access from API layer
- [ ] No swallowed exceptions
- [ ] No hardcoded secrets or config
- [ ] No god objects (classes doing too much)
- [ ] No magic numbers
- [ ] No sync calls blocking async flow
- [ ] Dependencies injected, not created inline
