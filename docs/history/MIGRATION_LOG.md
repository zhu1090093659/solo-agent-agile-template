# Migration Log

## Overview

This document tracks all database migrations and data migrations for audit and troubleshooting purposes.

---

## Database Migrations

### Migration Naming Convention

```
[YYYYMMDD]_[sequence]_[description].sql

Example: 20240115_001_create_users_table.sql
```

---

### Migration History

| Version | Date | Description | Reversible | Notes |
|---------|------|-------------|------------|-------|
| 001 | [Date] | Initial schema | Yes | Base tables |
| 002 | [Date] | Add user profiles | Yes | |
| 003 | [Date] | Add indexes | Yes | Performance |

---

### Migration Details

#### 001 - Initial Schema

**Date**: [Date]
**Author**: [Name]

**Changes**:
- Created `users` table
- Created `sessions` table

**SQL**:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Rollback**:
```sql
DROP TABLE users;
DROP TABLE sessions;
```

---

#### 002 - [Description]

**Date**: [Date]
**Author**: [Name]

**Changes**:
- [Change 1]
- [Change 2]

**Rollback considerations**:
[Any special notes about rolling back]

---

## Data Migrations

Data migrations that modify existing data (not just schema).

### [Date] - [Description]

**Purpose**: [Why this migration was needed]

**Script**: `scripts/migrations/[script_name].py`

**Data affected**:
- Table: [table]
- Rows affected: [count]

**Execution**:
```bash
python scripts/migrations/[script].py --dry-run  # Preview
python scripts/migrations/[script].py --execute  # Run
```

**Verification**:
```sql
-- Query to verify migration success
SELECT COUNT(*) FROM [table] WHERE [condition];
```

**Rollback**:
[Instructions for reverting, if possible]

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

# Check for locks
SELECT * FROM pg_locks WHERE NOT granted;
```

### Rollback needed

```bash
# Rollback last migration
make db-rollback

# Rollback to specific version
make db-rollback VERSION=003
```

### Stuck migration

```bash
# Force mark as complete (use with caution!)
make db-stamp VERSION=003
```

---

## Emergency Procedures

### Production Migration Failure

1. **Do not panic**
2. Check if application is affected
3. Review error logs
4. Decide: fix forward or rollback
5. If rollback: follow rollback procedure
6. If fix forward: test fix on staging first
7. Document in incident log

### Rollback Procedure

```bash
# 1. Verify current state
make db-status-prod

# 2. Run rollback
make db-rollback-prod

# 3. Verify rollback
make db-verify-prod

# 4. Restart application if needed
make restart-prod
```
