---
description: Systematic debugging assistance
---

You are entering debug mode. Let's systematically diagnose the issue.

## Issue Description

$ARGUMENTS

## Debugging Process

### 1. Understand the Problem

**Expected behavior**: [What should happen?]
**Actual behavior**: [What is happening?]
**Error message** (if any): [Exact error text]

### 2. Gather Context

Questions to answer:
- When did this start happening?
- What changed recently?
- Is it reproducible?
- Does it happen in all environments?

### 3. Check Common Causes

Reference: @docs/knowledge/TROUBLESHOOTING.md

| Possible Cause | Check | Result |
|----------------|-------|--------|
| [Cause 1] | [How to verify] | [TBD] |
| [Cause 2] | [How to verify] | [TBD] |
| [Cause 3] | [How to verify] | [TBD] |

### 4. Isolate the Problem

```
[Minimal reproduction steps]
1. 
2. 
3. 
```

### 5. Examine the Code

Files likely involved:
- [File 1]: [Why it might be related]
- [File 2]: [Why it might be related]

### 6. Form Hypothesis

**Most likely cause**: [Hypothesis]
**Evidence**: [What supports this]
**Test**: [How to verify]

### 7. Debug Commands

```bash
# Check logs
tail -f logs/app.log | grep -i error

# Check database
make db-status

# Run specific test
pytest tests/[relevant_test].py -v
```

### 8. Solution

Once found:
- [ ] Fix applied
- [ ] Test passes
- [ ] Add regression test
- [ ] Document in TROUBLESHOOTING.md (if new issue type)

---

Let's start debugging. What additional information can you provide?
