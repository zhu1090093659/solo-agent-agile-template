---
description: Break down a feature request into executable tasks
---

You are acting as a project manager. Please break down the following feature request into actionable tasks.

Feature Request: $ARGUMENTS

## Analysis Process

1. **Understand the Request**
   - What is the core functionality needed?
   - Who is the user/beneficiary?
   - What are the acceptance criteria?

2. **Check Existing Context**
   - Read @docs/architecture/OVERVIEW.md for system context
   - Read @docs/architecture/MODULES.md for module structure
   - Check if similar features exist

3. **Identify Scope**
   - What modules are affected?
   - What new components are needed?
   - What integrations are required?

## Task Breakdown

### Phase 1: [Phase Name] (Foundation)

| Task | Description | Est. | Dependencies |
|------|-------------|------|--------------|
| 1.1 | [Task] | [Xh] | None |
| 1.2 | [Task] | [Xh] | 1.1 |

**Phase 1 Deliverable**: [What's usable after this phase]

### Phase 2: [Phase Name] (Core)

| Task | Description | Est. | Dependencies |
|------|-------------|------|--------------|
| 2.1 | [Task] | [Xh] | Phase 1 |
| 2.2 | [Task] | [Xh] | 2.1 |

**Phase 2 Deliverable**: [What's usable after this phase]

### Phase 3: [Phase Name] (Polish)

| Task | Description | Est. | Dependencies |
|------|-------------|------|--------------|
| 3.1 | [Task] | [Xh] | Phase 2 |
| 3.2 | [Task] | [Xh] | 3.1 |

**Phase 3 Deliverable**: [Complete feature]

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | [N] |
| Total Estimated Time | [Xh] |
| Recommended Sessions | [N] |
| Risk Level | [Low/Medium/High] |

## Technical Considerations

### Architecture Impact
- [How this affects the system]

### Potential Risks
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

### Open Questions
- [Question that needs answering before starting]

---

## Next Steps

1. Review and adjust estimates
2. Create Epic folder: `epics/NN-[feature-name]/`
3. Copy task breakdown to `tasks.md`
4. Update ROADMAP.md with new Epic
5. Begin with Task 1.1
