---
description: Mark current task as complete and update all status documents
---

Task completion requested. I will now update all relevant documentation.

## Pre-Completion Checklist

Before marking complete, please confirm:

- [ ] Code changes are committed
- [ ] Tests pass (if applicable)
- [ ] Documentation updated (if applicable)

$ARGUMENTS

## Updates to Make

### 1. STATUS.md

Update the following sections:
- Move current task from "In Progress" to "What's Done This Session"
- Update the progress bar/percentage
- Set the next task as "Current Focus" (or clear if session ending)
- Add any new blockers or questions discovered
- Update "Last Updated" timestamp

### 2. Epic tasks.md

- Change task status from WIP to DONE
- Fill in "Actual" time column
- Add any notes about the completion

### 3. Epic notes.md

Add a session entry:
```
### [Today's Date] - Session [N]

**Completed**:
- [x] [Task that was just completed]

**Notes**:
- [Any learnings or observations]

**Next**:
- [ ] [What should be done next]
```

### 4. .claude/MEMORY.md (if needed)

Add any new persistent knowledge:
- Project quirks discovered
- Important decisions made
- Things to remember for future sessions

### 5. ROADMAP.md (if Epic completed)

If this was the last task in an Epic:
- Update Epic status from WIP to DONE
- Update overall release progress

## Summary

After updates:

**Completed**: [Task description]
**Time Taken**: [Actual vs Estimated]
**Epic Progress**: [X/Y tasks complete]
**Next Up**: [Next task or "End of session"]

---

Documentation has been updated.
