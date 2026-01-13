# External API Reference

> Renamed from: API_EXTERNAL.md

---

## Overview

Base URL: `http://localhost:8000/api`

All endpoints require authentication unless marked as public.

---

## Authentication

### Bearer Token

```
Authorization: Bearer <access_token>
```

### API Key (for server-to-server)

```
X-API-Key: <api_key>
```

---

## Common Response Format

### Success

```json
{
    "data": { ... },
    "meta": {
        "request_id": "uuid"
    }
}
```

### Error

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable message",
        "details": { ... }
    }
}
```

### Pagination

```json
{
    "data": [ ... ],
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "total_pages": 5
    }
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `AUTHENTICATION_REQUIRED` | 401 | Missing or invalid auth |
| `PERMISSION_DENIED` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Chat Endpoints

### POST /chat/sessions

Create a new chat session.

**Response**: `200 OK`
```json
{
    "session_id": "uuid",
    "message_count": 0
}
```

---

### GET /chat/sessions/{session_id}

Get session info.

**Response**: `200 OK`
```json
{
    "session_id": "uuid",
    "message_count": 5
}
```

**Errors**:
- `NOT_FOUND` - Session not found

---

### DELETE /chat/sessions/{session_id}

End and cleanup a chat session.

**Response**: `200 OK`
```json
{
    "status": "ok"
}
```

---

### POST /chat/message

Send a message and stream response via SSE.

**Request**:
```json
{
    "message": "Hello!",
    "session_id": "optional-uuid"
}
```

**Response**: Server-Sent Events stream

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

**Headers**:
```
X-Session-Id: uuid
```

---

### POST /chat/message/sync

Send a message and wait for complete response.

**Request**:
```json
{
    "message": "Hello!",
    "session_id": "optional-uuid"
}
```

**Response**: `200 OK`
```json
{
    "session_id": "uuid",
    "response": "Full response text..."
}
```

---

## Admin Endpoints

### POST /chat/admin/reload-prompt

Reload system prompt from file.

**Response**: `200 OK`
```json
{
    "status": "ok",
    "message": "Prompt reloaded"
}
```

---

### POST /chat/admin/set-persona

Switch agent persona.

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| persona | string | Persona name |

**Response**: `200 OK`
```json
{
    "status": "ok",
    "persona": "friendly"
}
```

---

## Rate Limits

| Tier | Limit | Window |
|------|-------|--------|
| Default | 100 | 1 minute |

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## SDK / Client Usage

### JavaScript/TypeScript

```javascript
// Using fetch with SSE
const response = await fetch('/api/chat/message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Hello!',
    session_id: 'optional-session-id'
  })
});

// Read SSE stream
const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const text = decoder.decode(value);
  // Parse SSE events...
}
```

### Python

```python
import httpx

async with httpx.AsyncClient() as client:
    async with client.stream(
        'POST',
        'http://localhost:8000/api/chat/message',
        json={'message': 'Hello!'}
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith('data: '):
                data = json.loads(line[6:])
                print(data)
```
