# Migration Log

## Overview

This document tracks all database migrations and data migrations for audit and troubleshooting purposes.

---

## Migration Naming Convention

```
[YYYYMMDD]_[sequence]_[description].sql

Example: 20240115_001_create_users_table.sql
```

---

## Migration History

| Version | Date | Description | Reversible | Notes |
|---------|------|-------------|------------|-------|
| 001 | [Date] | Initial schema | Yes | Base tables |

---

## Migration Details

### 001 - Initial Schema

**Date**: [Date]
**Author**: [Name]

**Changes**:
- Created base tables

**SQL**:
```sql
-- Example migration
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Rollback**:
```sql
DROP TABLE sessions;
```

---

## Schema Versions by Environment

| Environment | Schema Version | Last Migration | Date |
|-------------|----------------|----------------|------|
| Development | [version] | [migration] | [date] |
| Staging | [version] | [migration] | [date] |
| Production | [version] | [migration] | [date] |

---

## Migration Best Practices

### Before Creating a Migration

1. Check if similar migration exists
2. Consider backward compatibility
3. Plan for rollback
4. Estimate execution time for large tables

### Writing Migrations

- One logical change per migration
- Always include rollback script
- Test on copy of production data
- Add appropriate indexes

### Deploying Migrations

1. Run on development
2. Run on staging with production-like data
3. Take production backup
4. Run on production during low-traffic period
5. Verify success
6. Update this log

---

## Troubleshooting

### Migration fails

```bash
# Check migration status
make db-status

# View migration history
make db-history
```

### Rollback needed

```bash
# Rollback last migration
make db-rollback

# Rollback to specific version
make db-rollback VERSION=003
```
