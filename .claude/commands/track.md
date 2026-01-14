---
description: Create lightweight task tracking for medium complexity tasks (3-10 steps)
---

Create an Active Task in the current Epic's notes.md for tracking medium complexity tasks.

## Arguments

$ARGUMENTS = Task name/description

Example:
- `/project:track "Implement JWT refresh token"`
- `/project:track "Debug CORS issue"`
- `/project:track "Research caching options"`

---

## Step 1: Identify Current Epic

Read @STATUS.md to find the current Epic location.

If no Epic exists, suggest using `/project:init epic "name"` first.

---

## Step 2: Check for Existing Active Task

Read the current Epic's notes.md.

If an Active Task already exists:
- Display warning: "Active Task already exists"
- Ask: Complete it first, Abandon it, or Continue with new task?

---

## Step 3: Gather Task Information

Based on $ARGUMENTS, determine:

1. **Task Name**: Extract from arguments
2. **Goal**: One sentence describing the end state
3. **Phases**: Break into 2-4 phases (ask user if unclear)
4. **Key Questions**: What needs to be answered?

---

## Step 4: Create Active Task Section

Add to the current Epic's notes.md (at the top, before Session Log):

```markdown
## Active Task: [Task Name]

**Goal**: [Goal description]
**Started**: [Today's date]
**Status**: In Progress

### Phases
- [ ] Phase 1: [Name] - [Description]
- [ ] Phase 2: [Name] - [Description]
- [ ] Phase 3: [Name] - [Description]

### Key Questions
- [ ] [Question 1]
- [ ] [Question 2]

### Findings
| Finding | Source | Date |
|---------|--------|------|
| | | |

### Errors Encountered
| Error | Cause | Solution |
|-------|-------|----------|
| | | |

### Decisions Made
| Decision | Rationale | Date |
|----------|-----------|------|
| | | |

---
```

---

## Step 5: Output Confirmation

```markdown
## Active Task Created

**Task**: [Task Name]
**Location**: epics/[XX]-[name]/notes.md
**Phases**: [N] phases

### Next Steps
1. Start with Phase 1
2. Update Findings after every 2 operations (2-Action Rule)
3. Record any errors immediately
4. Use `/project:done "task" --findings "..." --error "..."` when complete

---
REMINDER: 2-Action Rule is now active
Every 2 view operations -> Update Findings table
```

---

## Completion

When user completes this task via `/project:done`:
- Archive Active Task section to Session Log
- Clear the Active Task section
- Update STATUS.md if needed

---

$ARGUMENTS
