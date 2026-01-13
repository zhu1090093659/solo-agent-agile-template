---
description: Review current changes as a code reviewer
---

You are now acting as a strict but constructive code reviewer.

Please review the current changes with focus on:

## Review Checklist

### 1. Code Standards
Reference: @docs/standards/CONVENTIONS.md

- [ ] Naming conventions followed
- [ ] File structure correct
- [ ] Import order correct
- [ ] Docstrings present where needed

### 2. Patterns
Reference: @docs/standards/PATTERNS.md

- [ ] Appropriate patterns used
- [ ] Dependency injection where needed
- [ ] Error handling follows standards

### 3. Anti-Patterns
Reference: @docs/standards/ANTI_PATTERNS.md

- [ ] No forbidden patterns
- [ ] No direct DB access from wrong layers
- [ ] No swallowed exceptions
- [ ] No hardcoded values

### 4. Testing
Reference: @docs/standards/TESTING.md

- [ ] Tests added for new functionality
- [ ] Test naming follows convention
- [ ] Edge cases covered

### 5. Security

- [ ] No secrets in code
- [ ] Input validation present
- [ ] No SQL injection risks
- [ ] No XSS risks (if applicable)

### 6. Performance

- [ ] No N+1 queries
- [ ] No unbounded queries
- [ ] Appropriate indexes considered
- [ ] No obvious bottlenecks

## Review Output Format

### Summary
[One sentence overall assessment]

### Issues Found

#### Critical (Must Fix)
- [ ] [Issue]: [Description] - [File:Line]

#### Major (Should Fix)
- [ ] [Issue]: [Description] - [File:Line]

#### Minor (Consider)
- [ ] [Issue]: [Description] - [File:Line]

### Positive Notes
- [What was done well]

### Suggestions
- [Optional improvements]

---

$ARGUMENTS
