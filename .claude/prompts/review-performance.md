# Performance Review Prompt

Review the following code for performance issues:

## Check For

### Database Queries
- [ ] No N+1 query patterns
- [ ] Queries use appropriate indexes
- [ ] No SELECT * (only needed columns)
- [ ] Pagination for list queries
- [ ] Appropriate use of joins vs separate queries

### Memory Usage
- [ ] No unbounded collections
- [ ] Large data processed in streams/chunks
- [ ] No memory leaks (unclosed resources)
- [ ] Appropriate data structure choices

### Algorithm Efficiency
- [ ] No unnecessary nested loops
- [ ] Appropriate data structures for lookups
- [ ] Early returns where possible
- [ ] No repeated expensive computations

### I/O Operations
- [ ] Async where beneficial
- [ ] Connection pooling used
- [ ] Appropriate timeouts set
- [ ] Retries with backoff

### Caching
- [ ] Expensive operations cached
- [ ] Cache invalidation handled
- [ ] Appropriate TTLs set

## Output Format

### Performance Issues Found

| Severity | Issue | Location | Impact | Fix |
|----------|-------|----------|--------|-----|
| HIGH | [Issue] | [File:Line] | [Impact] | [Fix] |
| MEDIUM | [Issue] | [File:Line] | [Impact] | [Fix] |
| LOW | [Issue] | [File:Line] | [Impact] | [Fix] |

### Optimization Recommendations

- [Recommendations for improving performance]

### Estimated Impact

- Current: [Estimate current performance]
- After fixes: [Estimate improvement]
