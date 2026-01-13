# Event Definitions

## Overview

This document defines all domain events used for async communication between modules.

---

## Event Naming Convention

```
[domain].[entity].[action]

Examples:
- user.account.created
- order.payment.completed
- inventory.stock.low
```

---

## Event Registry

### User Domain

#### user.account.created

**Trigger**: New user registration completed
**Producer**: UserService
**Payload**:

```python
{
    "event_type": "user.account.created",
    "timestamp": "2024-01-01T00:00:00Z",
    "data": {
        "user_id": "uuid",
        "email": "user@example.com",
        "registration_source": "web|api|oauth"
    }
}
```

**Consumers**:
| Consumer | Action |
|----------|--------|
| EmailService | Send welcome email |
| AnalyticsService | Track signup |

---

#### user.account.deleted

**Trigger**: User account deletion
**Producer**: UserService
**Payload**:

```python
{
    "event_type": "user.account.deleted",
    "timestamp": "2024-01-01T00:00:00Z",
    "data": {
        "user_id": "uuid",
        "deletion_reason": "user_request|admin|inactivity"
    }
}
```

**Consumers**:
| Consumer | Action |
|----------|--------|
| DataCleanupService | Remove user data |
| BillingService | Cancel subscriptions |

---

### [Domain] Domain

#### [domain].[entity].[action]

**Trigger**: [When this event fires]
**Producer**: [Service that publishes]
**Payload**:

```python
{
    "event_type": "[domain].[entity].[action]",
    "timestamp": "ISO8601",
    "data": {
        # payload fields
    }
}
```

**Consumers**:
| Consumer | Action |
|----------|--------|
| [Service] | [What it does] |

---

## Event Infrastructure

### Publishing Events

```python
from core.events import event_bus

# Publish an event
await event_bus.publish(
    "user.account.created",
    user_id=user.id,
    email=user.email
)
```

### Subscribing to Events

```python
from core.events import event_bus

@event_bus.subscribe("user.account.created")
async def handle_user_created(event: Event):
    user_id = event.data["user_id"]
    # Handle event
```

---

## Event Guarantees

| Property | Guarantee |
|----------|-----------|
| Delivery | At least once |
| Ordering | Per-entity ordered |
| Retention | 7 days |

---

## Error Handling

Failed event handlers:
1. Log error with full context
2. Retry with exponential backoff (3 attempts)
3. Move to dead letter queue
4. Alert on threshold exceeded

---

## Adding New Events

1. Define event in this document
2. Create payload schema in `src/modules/core/events/schemas/`
3. Register in event catalog
4. Document all consumers
5. Add monitoring/alerting
