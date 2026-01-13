# Security Review Prompt

Review the following code for security vulnerabilities:

## Check For

### Input Validation
- [ ] All user inputs validated
- [ ] Input length limits enforced
- [ ] Special characters handled

### Authentication & Authorization
- [ ] Authentication required where needed
- [ ] Authorization checks in place
- [ ] Session handling secure

### Injection Attacks
- [ ] SQL injection prevented (parameterized queries)
- [ ] Command injection prevented
- [ ] XSS prevented (output encoding)
- [ ] LDAP injection prevented

### Data Protection
- [ ] Sensitive data encrypted
- [ ] Passwords hashed properly
- [ ] PII handled correctly
- [ ] Logs don't contain secrets

### Configuration
- [ ] No hardcoded secrets
- [ ] Secure defaults
- [ ] Error messages don't leak info

### Dependencies
- [ ] No known vulnerable packages
- [ ] Packages from trusted sources

## Output Format

### Vulnerabilities Found

| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| CRITICAL | [Issue] | [File:Line] | [Fix] |
| HIGH | [Issue] | [File:Line] | [Fix] |
| MEDIUM | [Issue] | [File:Line] | [Fix] |
| LOW | [Issue] | [File:Line] | [Fix] |

### Security Recommendations

- [General recommendations]
