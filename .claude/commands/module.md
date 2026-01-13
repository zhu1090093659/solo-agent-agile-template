---
description: Load context for a specific module
---

Loading context for module: $ARGUMENTS

Please read the following files for this module:

1. **Module Overview**: src/modules/$ARGUMENTS/MODULE.md
   - Understand module responsibility
   - Note dependencies (what it uses, what uses it)
   - Identify entry points

2. **Public Interface**: src/modules/$ARGUMENTS/INTERFACE.md
   - Understand the public contract
   - Note DTOs and exceptions
   - Understand what other modules expect

3. **Internal Details**: src/modules/$ARGUMENTS/INTERNALS.md
   - Understand implementation details
   - Note performance considerations
   - Check known issues

4. **Related Standards**:
   - @docs/standards/CONVENTIONS.md for coding standards
   - @docs/knowledge/GLOSSARY.md for terminology

5. **Check for Active Work**:
   - @STATUS.md to see if there's current work in this module

## Module Context Summary

### Module: $ARGUMENTS

**Responsibility**: [From MODULE.md]

**Key Classes**:
- [Class 1]: [Purpose]
- [Class 2]: [Purpose]

**Dependencies**:
- Uses: [modules this depends on]
- Used by: [modules that depend on this]

**Entry Points**:
| Entry | Location | Purpose |
|-------|----------|---------|
| [Entry] | [File] | [Purpose] |

**Current Tech Debt**:
- [Debt item if any]

**Gotchas**:
- [Important things to know]

---

Ready to work on this module.
