---
description: Mark task complete (supports --log and --doc options)
---

Mark current task as complete and update status documents.

## Arguments

Parse $ARGUMENTS for:
- Main content: Task completion description
- `--log "notes"`: Also record session notes to Epic/notes.md
- `--doc`: Also update relevant docs/ based on task type

Examples:
- `/project:done "Completed user auth API"`
- `/project:done "Added caching layer" --log "Redis works better than memcached"`
- `/project:done "Refactored database module" --doc`

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
- Fill in "Actual" time column
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

## Summary Output

After all updates:

**Completed**: [Task description]
**Time Taken**: [Actual vs Estimated]
**Epic Progress**: [X/Y tasks complete]
**Docs Updated**: [List of docs touched, or "None"]
**Next Up**: [Next task or "End of session"]

---

$ARGUMENTS
