---
description: Plan feature tasks (supports --design and --full modes)
---

Break down a feature request into actionable tasks, with optional architecture design.

## Arguments

Parse $ARGUMENTS for:
- Main content: Feature/problem description
- `--design`: Architecture design perspective (no task breakdown)
- `--full`: Complete analysis (design + task breakdown)

Examples:
- `/project:plan "Add user authentication"` → Task breakdown only
- `/project:plan "How to add caching?" --design` → Architecture design only
- `/project:plan "Payment integration" --full` → Design + tasks

---

## Step 1: Check Existing Context

- Read @docs/architecture/OVERVIEW.md for system context
- Read @docs/architecture/MODULES.md for module structure
- Check if similar features exist

---

## Step 2: Output Based on Mode

### Default Mode (Task Breakdown)

If $ARGUMENTS does NOT contain `--design`:

#### Analysis

1. **Understand the Request**
   - What is the core functionality needed?
   - Who is the user/beneficiary?
   - What are the acceptance criteria?

2. **Identify Scope**
   - What modules are affected?
   - What new components are needed?

#### Task Breakdown

### Phase 1: [Phase Name] (Foundation)

| Task | Description | Dependencies |
|------|-------------|--------------|
| 1.1 | [Task] | None |
| 1.2 | [Task] | 1.1 |

**Phase 1 Deliverable**: [What's usable after this phase]

### Phase 2: [Phase Name] (Core)

| Task | Description | Dependencies |
|------|-------------|--------------|
| 2.1 | [Task] | Phase 1 |
| 2.2 | [Task] | 2.1 |

**Phase 2 Deliverable**: [What's usable after this phase]

### Phase 3: [Phase Name] (Polish)

| Task | Description | Dependencies |
|------|-------------|--------------|
| 3.1 | [Task] | Phase 2 |
| 3.2 | [Task] | 3.1 |

**Phase 3 Deliverable**: [Complete feature]

#### Summary

| Metric | Value |
|--------|-------|
| Total Tasks | [N] |
| Risk Level | [Low/Medium/High] |

#### Next Steps

1. Create Epic: `epics/NN-[feature-name]/`
2. Copy tasks to `tasks.md`
3. Update ROADMAP.md
4. Begin with Task 1.1

---

### Design Mode (--design)

If $ARGUMENTS contains `--design`:

Act as a Software Architect. Provide design guidance WITHOUT writing code.

#### 1. Problem Understanding

[Restate the problem and clarify requirements]

#### 2. Current State

Reference existing architecture. How does this fit?

#### 3. Proposed Design

```
[ASCII diagram of proposed solution]
```

**Components**:

| Component | Responsibility | Interface |
|-----------|---------------|-----------|
| [Component] | [What it does] | [How to interact] |

**Data Flow**:
```
[Input] -> [Step 1] -> [Step 2] -> [Output]
```

#### 4. Module Impact

| Module | Change Type | Complexity |
|--------|-------------|------------|
| [Module] | [New/Modify/None] | [Low/Med/High] |

#### 5. Interface Design

```
Service: [Name]
  - method1(input) -> output
  - method2(input) -> output
```

#### 6. Trade-offs

| Option | Pros | Cons |
|--------|------|------|
| [Option A] | [Pros] | [Cons] |
| [Option B] | [Pros] | [Cons] |

**Recommendation**: [Which option and why]

#### 7. Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| [Risk] | [H/M/L] | [How to handle] |

---

### Full Mode (--full)

If $ARGUMENTS contains `--full`:

Output BOTH sections:
1. First, the Design Mode output (architecture analysis)
2. Then, the Default Mode output (task breakdown)

This provides a complete picture: design decisions followed by actionable tasks.

---

## Before Implementing (Always Include)

Add this checklist at the end of every plan output:

### Pre-Implementation Checklist

Before starting implementation:

- [ ] Run `/project:context` to refresh current state
- [ ] Check @docs/LEARNINGS.md for related past issues
- [ ] Confirm this design aligns with original goal in EPIC.md
- [ ] Consider creating Active Task with `/project:track` for medium complexity work

---

$ARGUMENTS
