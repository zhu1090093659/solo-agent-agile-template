# Data Flow Architecture

## Request/Response Flow

### Typical API Request

```mermaid
flowchart TB
    Client[Client Request] --> Gateway
    
    subgraph Gateway[API Gateway]
        Auth[Authentication]
        Rate[Rate Limiting]
    end
    
    Gateway --> Controller
    
    subgraph Controller[Controller Layer]
        Valid[Request Validation]
        Route[Routing]
    end
    
    Controller --> Service
    
    subgraph Service[Service Layer]
        BL[Business Logic]
    end
    
    Service --> Repo
    
    subgraph Repo[Repository Layer]
        DA[Data Access]
    end
    
    Repo --> DB[(Database)]
```

---

## Data Transformation

### Input Flow

```mermaid
flowchart TB
    Raw[Raw HTTP Request] --> Validation
    Validation -->|Invalid| Error[ValidationError]
    Validation -->|Valid| DTO[DTO/Schema]
    DTO --> Domain[Domain Model]
    Domain --> Repository
    Repository --> DB[(Database)]
```

### Output Flow

```mermaid
flowchart TB
    DB[(Database)] --> Repository
    Repository --> Domain[Domain Model]
    Domain --> DTO[DTO/Schema]
    DTO --> Serial[Serialization]
    Serial --> Response[HTTP Response JSON]
```

---

## Event Flow (if applicable)

```mermaid
flowchart LR
    Producer([Producer]) --> Bus[Event Bus]
    Bus --> A[Handler A]
    Bus --> B[Handler B]
    A --> EA[Side Effect A]
    B --> EB[Side Effect B]
```

### Event Types

| Event | Producer | Consumers | Payload |
|-------|----------|-----------|---------|
| `user.created` | UserService | EmailService, AnalyticsService | `{user_id, email}` |
| `order.completed` | OrderService | InventoryService, NotificationService | `{order_id, items}` |

---

## External Integrations

### Outbound

| Service | Purpose | Data Sent | Frequency |
|---------|---------|-----------|-----------|
| [Service Name] | [Purpose] | [Data types] | [Sync/Async, rate] |

### Inbound

| Source | Purpose | Data Received | Handler |
|--------|---------|---------------|---------|
| [Source] | [Purpose] | [Data types] | [Handler location] |

---

## Caching Strategy

### Cache Layers

```mermaid
flowchart LR
    Request([Request]) --> L1[L1 Local Cache]
    L1 -->|Miss| L2[L2 Redis]
    L2 -->|Miss| DB[(Database)]
    DB --> L2
    L2 --> L1
    L1 --> Response([Response])
```

### Cache Keys

| Pattern | TTL | Invalidation |
|---------|-----|--------------|
| `user:{id}` | 1h | On user update |
| `config:*` | 24h | Manual refresh |

---

## Error Handling Flow

```mermaid
flowchart TB
    Ex[Exception Raised] --> Handler[Exception Handler]
    Handler --> Log[Log Error]
    Handler --> Mapper[Error Mapper]
    Mapper --> Status[Map to HTTP Status]
    Status --> Response[Error Response]
    Response --> Client([Return to Client])
```

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": {}
  }
}
```
