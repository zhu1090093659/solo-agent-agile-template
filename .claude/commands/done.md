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

---

## 6. docs/ Updates (NEW - Auto-Update)

Based on the completed task, update the relevant documentation in `docs/`. Follow these rules:

### Update Rules by Task Type

| If task involves... | Update this doc | What to add |
|---------------------|-----------------|-------------|
| New/modified API endpoint | `docs/API.md` | Endpoint spec, request/response format |
| Architecture change | `docs/ARCHITECTURE.md` | Component, flow, or diagram update |
| New module interface | `docs/INTERFACES.md` | Contract definition, event type |
| New business concept | `docs/DOMAIN.md` | Term definition, business rule |
| Solved tricky issue | `docs/TROUBLESHOOTING.md` | Issue, symptoms, solution |
| Env config change | `docs/SETUP.md` | New variable, dependency |
| Deploy process change | `docs/DEPLOY.md` | Step update, new requirement |
| Code convention update | `docs/CONVENTIONS.md` | New convention, example |
| Design pattern applied | `docs/PATTERNS.md` | Pattern usage, context |
| Test strategy change | `docs/TESTING.md` | New approach, fixture |
| Database migration | `docs/MIGRATION_LOG.md` | Migration entry |
| Important lesson | `docs/LEARNINGS.md` | Learning entry |
| Significant decision | `docs/decisions/NNN-xxx.md` | New ADR file |

### Update Format

When updating docs, follow these principles:

1. **简明扼要** - Keep updates brief and focused
   - One-liner for simple additions
   - Short paragraph for complex changes
   
2. **标准格式** - Follow existing document structure
   - Use the same heading levels
   - Match table formats
   - Follow code block conventions

3. **关联任务** - Reference the task
   ```
   <!-- Added: Epic XX, Task YY - [Date] -->
   ```

4. **时间戳** - Include date for traceability

### Example Updates

**API.md** - New endpoint:
```markdown
### POST /chat/admin/clear-cache

Clear agent cache. [Admin only]

**Response**: `200 OK`
```json
{"status": "ok", "cleared": 15}
```
<!-- Added: Epic 02, Task 03 - 2024-01-15 -->
```

**TROUBLESHOOTING.md** - New issue:
```markdown
#### Issue: Session timeout during long operations

**Symptoms**: SSE connection drops after 60s

**Solution**: Increase nginx proxy_read_timeout
```nginx
proxy_read_timeout 300s;
```
<!-- Added: Epic 02, Task 05 - 2024-01-15 -->
```

**LEARNINGS.md** - New learning:
```markdown
### 2024-01-15: SSE and Nginx Buffering

**What happened**: SSE responses were buffered

**What we learned**: Need `proxy_buffering off` for SSE

**Action taken**: Updated nginx.conf template
```

---

## Summary

After updates:

**Completed**: [Task description]
**Time Taken**: [Actual vs Estimated]
**Epic Progress**: [X/Y tasks complete]
**Docs Updated**: [List of docs touched]
**Next Up**: [Next task or "End of session"]

---

Documentation has been updated.
