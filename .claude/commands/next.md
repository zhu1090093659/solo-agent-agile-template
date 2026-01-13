---
description: Analyze project status and recommend next task
---

Please analyze the current project status and recommend the next task to work on:

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
**Estimated Time**: [From tasks.md or your estimate]
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

Ready to start when you are.
