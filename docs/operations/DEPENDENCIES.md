# Dependencies

## Overview

This document explains the third-party dependencies used in this project, why they were chosen, and any important notes about their usage.

---

## Dependency Philosophy

1. **Minimize dependencies**: Only add what's truly needed
2. **Prefer well-maintained packages**: Active development, good documentation
3. **Pin versions**: Use exact versions for reproducibility
4. **Document choices**: Explain why each dependency was chosen

---

## Core Dependencies

### [Framework Name]

**Package**: `[package-name]`
**Version**: `[version]`
**Purpose**: Web framework / ORM / etc.
**Documentation**: [link]

**Why chosen**:
- [Reason 1]
- [Reason 2]

**Alternatives considered**:
| Alternative | Why not chosen |
|-------------|----------------|
| [Package] | [Reason] |

---

### Database

**Package**: `[package-name]`
**Version**: `[version]`
**Purpose**: Database driver / ORM

**Configuration notes**:
```python
# Important configuration settings
POOL_SIZE = 5
MAX_OVERFLOW = 10
```

---

### Authentication

**Package**: `[package-name]`
**Version**: `[version]`
**Purpose**: JWT / OAuth / etc.

**Security notes**:
- [Important security consideration]

---

## Development Dependencies

### Testing

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | [ver] | Test runner |
| pytest-cov | [ver] | Coverage reporting |
| pytest-asyncio | [ver] | Async test support |

### Linting & Formatting

| Package | Version | Purpose |
|---------|---------|---------|
| black | [ver] | Code formatter |
| ruff | [ver] | Linter |
| mypy | [ver] | Type checker |

### Development Tools

| Package | Version | Purpose |
|---------|---------|---------|
| [package] | [ver] | [purpose] |

---

## External Services

### [Service Name]

**SDK**: `[package-name]`
**Version**: `[version]`
**Purpose**: [What we use it for]
**Documentation**: [link]

**Usage pattern**:
```python
from [package] import Client

client = Client(api_key=config.API_KEY)
```

**Rate limits**:
| Tier | Limit |
|------|-------|
| Free | 100/min |
| Pro | 1000/min |

---

## Version Constraints

### Why we pin versions

All dependencies are pinned to exact versions to ensure:
- Reproducible builds
- No surprise breaking changes
- Security audit trail

### Updating dependencies

```bash
# Check for updates
make check-deps

# Update a specific package
pip install --upgrade [package]

# Update all (with testing)
make update-deps
make test
```

---

## Known Issues

### [Package Name]

**Issue**: [Description of known issue]
**Workaround**: [How we work around it]
**Tracking**: [Link to issue]

---

## Security Considerations

### Vulnerability Scanning

```bash
# Scan for vulnerabilities
make security-scan

# Or using pip-audit
pip-audit
```

### Security Updates

Critical security updates should be applied immediately:

1. Check vulnerability details
2. Test update in development
3. Deploy to staging
4. Deploy to production

---

## License Compliance

All dependencies must have compatible licenses.

| License | Compatible | Notes |
|---------|------------|-------|
| MIT | Yes | Most permissive |
| Apache 2.0 | Yes | Patent grant included |
| BSD | Yes | Similar to MIT |
| GPL | Caution | Copyleft requirements |
| AGPL | No | Too restrictive |

### Checking licenses

```bash
# List all licenses
pip-licenses --format=markdown

# Check for problematic licenses
pip-licenses --fail-on="GPL"
```

---

## Adding New Dependencies

Before adding a new dependency:

1. **Justify the need**: Can we implement it ourselves?
2. **Evaluate options**: Compare alternatives
3. **Check maintenance**: Last commit, open issues, contributors
4. **Check license**: Must be compatible
5. **Security review**: Check for known vulnerabilities
6. **Document**: Add to this file with rationale

---

## Dependency Tree

```bash
# View full dependency tree
pipdeptree

# Check for conflicts
pipdeptree --warn fail
```
