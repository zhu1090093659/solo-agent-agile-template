---
description: Load current work context (supports standup/brief modes)
---

Load the current development context. Supports multiple output modes via $ARGUMENTS:
- `standup` → Standup report format (Yesterday/Today/Blockers)
- `brief` → Quick status only
- (empty) → Full context (default)

## Step 1: Read Context Files

1. Read @STATUS.md to understand:
   - What task is currently in progress
   - What was completed in the last session
   - Any blockers or open questions
   - What the next steps are

2. Based on STATUS.md, identify the current Epic and read:
   - The Epic's EPIC.md for overall goals
   - The Epic's tasks.md for specific task status
   - The Epic's notes.md for any recent learnings

3. Read @ROADMAP.md for overall release progress

4. Check @.claude/MEMORY.md for persistent notes (if exists)

5. Check @docs/LEARNINGS.md for relevant learnings:
   - Search for keywords related to current task/Epic
   - If found, prepare "Relevant Learnings" section for output

6. Check current Epic's notes.md for Active Task:
   - If Active Task section exists, note its status
   - Prepare reminder to continue or complete it

---

## Step 2: Output Based on Mode

### If $ARGUMENTS is empty or not "standup"/"brief" → Full Mode

## Current Context

**Epic**: [Name and current status]
**Task**: [Current task being worked on]
**Last Session**: [Brief summary of what was done]
**Blockers**: [Any blockers, or "None"]

## Active Task (if exists)

> Only show this section if an Active Task was found in notes.md

**Task**: [Active Task name]
**Progress**: [Current phase]
**Started**: [Date]
**Action Required**: Continue working, Complete it, or Abandon?

## Relevant Learnings (if found)

> Only show this section if related learnings were found in LEARNINGS.md

**Past Issue**: [Issue title]
**Solution**: [Brief solution]
**Tip**: Review this before starting similar work

## Ready to Continue

[What should be done next based on the context]

## Files Likely to Touch

- [List of files that will probably need modification]

---

I am now ready for your instructions.

---

### If $ARGUMENTS contains "standup" → Standup Mode

## Standup Report

### Yesterday/Last Session

- [Completed item 1 from STATUS.md]
- [Completed item 2]

### Today/This Session

- [ ] [Planned item 1 from Next Up]
- [ ] [Planned item 2]

### Blockers

[List any blockers, or "None"]

---

### Progress Overview

**Current Epic**: [Name] - [##########----------] XX% (X/Y tasks)

**Release Progress**:
```
Epic 1: [##########] 100% DONE
Epic 2: [########--]  80% IN PROGRESS
Epic 3: [----------]   0% TODO
```

**Target Date**: [From ROADMAP.md] | **On Track**: [Yes/No/At Risk]

---

### If $ARGUMENTS contains "brief" → Brief Mode

## Quick Status

**Epic**: [Name] ([X]% complete)
**Task**: [Current task]
**Status**: [In Progress / Blocked / Ready]
**Next**: [Immediate next action]

---

$ARGUMENTS
