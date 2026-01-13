# Glossary

## Purpose

This glossary ensures consistent terminology across code, documentation, and communication. When naming variables, classes, database tables, or API endpoints, use these terms exactly as defined.

---

## Core Business Terms

| Term | Definition | Usage Notes |
|------|------------|-------------|
| User | An individual with an account in the system | Not "customer", "member", or "account" |
| [Term] | [Definition] | [Notes] |

---

## Entity Terms

### User-Related

| Term | Definition | Code Usage |
|------|------------|------------|
| User | A registered individual | `User`, `user_id` |
| Account | The user's billing/subscription entity | `Account`, `account_id` |
| Profile | User's public-facing information | `UserProfile`, `profile_id` |
| Session | An authenticated login session | `Session`, `session_id` |

### [Domain]-Related

| Term | Definition | Code Usage |
|------|------------|------------|
| [Term] | [Definition] | [How to use in code] |

---

## Status Values

### Order Status

| Status | Meaning | Can Transition To |
|--------|---------|-------------------|
| draft | Order not yet submitted | pending, cancelled |
| pending | Awaiting processing | processing, cancelled |
| processing | Being fulfilled | completed, failed |
| completed | Successfully fulfilled | refunded |
| cancelled | Cancelled before processing | - |
| failed | Processing failed | pending (retry) |
| refunded | Money returned | - |

### [Entity] Status

| Status | Meaning | Can Transition To |
|--------|---------|-------------------|
| [status] | [meaning] | [transitions] |

---

## Technical Terms

| Term | Definition | Context |
|------|------------|---------|
| Repository | Data access layer | Code architecture |
| Service | Business logic layer | Code architecture |
| DTO | Data Transfer Object | API layer |
| Entity | Domain object with identity | Domain layer |
| Value Object | Immutable domain object | Domain layer |

---

## Abbreviations

| Abbr | Full Form | Context |
|------|-----------|---------|
| API | Application Programming Interface | General |
| CRUD | Create, Read, Update, Delete | Database operations |
| DTO | Data Transfer Object | Code |
| ID | Identifier | General |
| TX | Transaction | Payment/Database |
| UUID | Universally Unique Identifier | IDs |

---

## Naming Conventions

### In Code

| Context | Convention | Example |
|---------|------------|---------|
| Class names | PascalCase | `UserService` |
| Function names | snake_case | `get_user_by_id` |
| Variables | snake_case | `user_email` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Database tables | snake_case, plural | `user_accounts` |
| API endpoints | kebab-case | `/user-profiles` |

### In Documentation

| Context | Convention | Example |
|---------|------------|---------|
| Referring to code | backticks | `UserService` |
| File paths | backticks | `src/modules/user/` |
| Concepts | normal text | user service |

---

## Confusing Terms Clarification

### User vs Account vs Profile

- **User**: The authentication entity (login credentials)
- **Account**: The billing entity (subscription, payment)
- **Profile**: The public-facing entity (display name, avatar)

One User has one Account and one Profile.

### [Term A] vs [Term B]

- **[Term A]**: [When to use this]
- **[Term B]**: [When to use this]

---

## Domain-Specific Jargon

Terms specific to this industry/domain:

| Term | Definition | Example |
|------|------------|---------|
| [Industry term] | [What it means in this context] | [Example usage] |

---

## Deprecated Terms

Terms that should no longer be used:

| Deprecated | Use Instead | Reason |
|------------|-------------|--------|
| [old term] | [new term] | [why changed] |

---

## Adding New Terms

When adding a new term:

1. Check if a similar term already exists
2. Define clearly with usage context
3. Add code examples if applicable
4. Update relevant documentation
5. Notify team of new terminology
