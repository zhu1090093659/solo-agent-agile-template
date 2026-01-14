---
description: Mark task complete (supports --log, --doc, --findings, --error options)
---

Mark current task as complete and update status documents.

## Arguments

Parse $ARGUMENTS for:
- Main content: Task completion description
- `--log "notes"`: Record session notes to Epic/notes.md
- `--doc`: Update relevant docs/ based on task type
- `--findings "discoveries"`: Save research findings to notes.md
- `--error "issue"`: Record error/learning to docs/LEARNINGS.md

Examples:
- `/project:done "Completed user auth API"`
- `/project:done "Added caching layer" --log "Redis works better than memcached"`
- `/project:done "Refactored database module" --doc`
- `/project:done "Fixed CORS issue" --findings "Need credentials:true" --error "CORS blocked due to missing header"`

---

## Pre-Completion Checklist

Before marking complete, please confirm:

- [ ] Code changes are committed
- [ ] Tests pass (if applicable)

---

## Required Updates (Always)

### 1. STATUS.md

- Move current task to "What's Done This Session"
- Update progress bar/percentage
- Set next task as "Current Focus" (or clear if session ending)
- Update "Last Updated" timestamp

### 2. Epic tasks.md

- Change task status from WIP to DONE
- Fill in "Completed" date column
- Add completion notes if any

### 3. ROADMAP.md (if Epic completed)

If this was the last task in an Epic:
- Update Epic status from WIP to DONE
- Update overall release progress

---

## Optional: --log (Session Notes)

If $ARGUMENTS contains `--log`:

### Update Epic notes.md

Add a session entry:
```
### [Today's Date] - Session [N]

**Completed**:
- [x] [Task that was just completed]

**Notes**:
- [Extract notes from --log argument]

**Next**:
- [ ] [What should be done next]
```

### Update .claude/MEMORY.md (if important)

Add persistent knowledge if discovered:
- Project quirks
- Important decisions
- Things to remember

---

## Optional: --doc (Documentation Update)

If $ARGUMENTS contains `--doc`:

Based on the completed task type, suggest and update relevant docs:

| Task Type | Update Doc | What to Add |
|-----------|------------|-------------|
| API endpoint | `docs/interfaces/API.md` | Endpoint spec |
| Architecture | `docs/architecture/OVERVIEW.md` | Component update |
| New module | `docs/architecture/MODULES.md` | Module description |
| Tricky issue | `docs/operations/TROUBLESHOOTING.md` | Issue & solution |
| Config change | `docs/operations/SETUP.md` | New variable |
| Important decision | `docs/decisions/NNN-xxx.md` | New ADR |

Update format:
```markdown
<!-- Added: Epic XX, Task YY - [Date] -->
[Content]
```

---

## Optional: --findings (Research Findings)

If $ARGUMENTS contains `--findings`:

Add to current Epic's notes.md in the Research Notes section (create if not exists):

```markdown
### [Today's Date]: [Task Name]

**Findings**:
- [Extract findings from --findings argument]

**Context**: [Brief description of what was being done]
```

If an Active Task exists, also update its Findings table.

---

## Optional: --error (Error Recording)

If $ARGUMENTS contains `--error`:

Add to @docs/LEARNINGS.md in the Technical Learnings section:

```markdown
### [Today's Date]: [Short title from error description]

**What happened**:
[Current task context - what were you trying to do]

**What we learned**:
[Extract error description from --error argument]

**Action taken**:
[How it was resolved]

**Related**: Epic [XX], Task [YY]
```

Also update the Quick Lookup Index table if it exists.

---

## Active Task Handling

Check if an Active Task exists in the current Epic's notes.md.

If Active Task exists and matches the completed task:
1. Mark Active Task as complete
2. Archive the Active Task section to Session Log
3. Clear the Active Task section

Archive format:
```markdown
### [Today's Date] - Completed Active Task

**Task**: [Task Name]
**Duration**: [Started] ~ [Completed]
**Findings**: [Summary of findings]
**Errors**: [Summary of errors encountered]
```

---

## Summary Output

After all updates:

**Completed**: [Task description]
**Time**: [Started] ~ [Completed]
**Epic Progress**: [X/Y tasks complete]
**Docs Updated**: [List of docs touched, or "None"]
**Next Up**: [Next task or "End of session"]

---

$ARGUMENTS
