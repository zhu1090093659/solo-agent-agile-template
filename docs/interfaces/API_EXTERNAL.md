# External API Reference

## Overview

Base URL: `https://api.[domain].com/v1`

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
    },
    "meta": {
        "request_id": "uuid"
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

## Endpoints

### Users

#### GET /users/me

Get current authenticated user.

**Response**:
```json
{
    "data": {
        "id": "uuid",
        "email": "user@example.com",
        "name": "User Name",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

---

#### POST /users

Create new user. [PUBLIC]

**Request**:
```json
{
    "email": "user@example.com",
    "password": "securepassword",
    "name": "User Name"
}
```

**Response**: `201 Created`
```json
{
    "data": {
        "id": "uuid",
        "email": "user@example.com",
        "name": "User Name"
    }
}
```

**Errors**:
- `VALIDATION_ERROR` - Invalid input
- `CONFLICT` - Email already exists

---

### [Resource]

#### GET /[resources]

List [resources] with pagination.

**Query Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | int | 1 | Page number |
| per_page | int | 20 | Items per page (max 100) |
| sort | string | created_at | Sort field |
| order | string | desc | Sort order (asc/desc) |

**Response**: `200 OK`
```json
{
    "data": [ ... ],
    "pagination": { ... }
}
```

---

#### GET /[resources]/{id}

Get single [resource] by ID.

**Response**: `200 OK`
```json
{
    "data": { ... }
}
```

**Errors**:
- `NOT_FOUND` - Resource not found

---

#### POST /[resources]

Create new [resource].

**Request**:
```json
{
    // fields
}
```

**Response**: `201 Created`

---

#### PUT /[resources]/{id}

Update [resource].

**Request**:
```json
{
    // fields to update
}
```

**Response**: `200 OK`

---

#### DELETE /[resources]/{id}

Delete [resource].

**Response**: `204 No Content`

---

## Rate Limits

| Tier | Limit | Window |
|------|-------|--------|
| Free | 100 | 1 minute |
| Pro | 1000 | 1 minute |
| Enterprise | Custom | Custom |

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## Webhooks

### Configuration

```json
{
    "url": "https://your-server.com/webhook",
    "events": ["user.created", "order.completed"],
    "secret": "webhook_secret"
}
```

### Payload

```json
{
    "event": "user.created",
    "timestamp": "2024-01-01T00:00:00Z",
    "data": { ... }
}
```

### Verification

```
X-Signature: sha256=<hmac_signature>
```

---

## SDK / Client Libraries

- Python: `pip install [project]-client`
- JavaScript: `npm install @[org]/[project]-client`
