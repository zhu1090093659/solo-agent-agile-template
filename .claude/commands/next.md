---
description: Analyze project status and recommend next task
---

Please analyze the current project status and recommend the next task to work on:

0. **Check for Active Task first**:
   - Read current Epic's notes.md
   - If Active Task section exists:
     - Display "Active Task Reminder" (see format below)
     - Ask user: Continue, Complete, or Abandon?
     - Only proceed to step 1 if user chooses to abandon or no Active Task exists

1. Read @STATUS.md to understand current state

2. Look at the current Epic's tasks.md:
   - Find the first TODO task that has no blockers
   - Check if any WIP tasks need to be completed first

3. If current Epic is complete, check @ROADMAP.md for:
   - Next Epic in the current release
   - Any high-priority items

4. Consider dependencies:
   - Does this task depend on something incomplete?
   - Will this task unblock other tasks?

## Recommendation Format

### Next Task

**Epic**: [Epic name]
**Task ID**: [Task ID from tasks.md]
**Task**: [Task description]
**Priority**: [Why this is the right next task]

### Prerequisites

- [x] [Already completed prerequisite]
- [x] [Another completed prerequisite]
- [ ] [Any missing prerequisite - flag if blocking]

### Getting Started

1. [First step to begin this task]
2. [Second step]
3. [Third step]

### Files to Modify

- `path/to/file1.py` - [What needs to change]
- `path/to/file2.py` - [What needs to change]

### Success Criteria

From the task definition:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Active Task Reminder Format

> Only show this if an Active Task was found in step 0

### Active Task Found

**Task**: [Active Task name from notes.md]
**Progress**: [Current phase status]
**Started**: [Date]
**Last Updated**: [Date of last Findings entry]

**Options**:
1. **Continue** - Resume working on this task
2. **Complete** - Mark it done with `/project:done "task" --findings "..." --error "..."`
3. **Abandon** - Archive incomplete and proceed to next task

What would you like to do?

---

Ready to start when you are.
