---
description: Initialize project or create new Epic
---

Initialize a new project or create a new Epic.

## Arguments

Parse $ARGUMENTS for mode:
- `epic "description"` → Create new Epic only
- Other → Full project initialization

Examples:
- `/project:init I want to build a habit tracking app` → Full init
- `/project:init epic "User Authentication"` → Create Epic only

---

## Mode 1: Create Epic (if $ARGUMENTS starts with "epic")

Create a new Epic without full project initialization.

### Step 1: Determine Epic Number

Check `epics/` folder for existing epics and determine next number (NN).

### Step 2: Gather Epic Information

If not provided, ask for:
1. **Epic Name**: Short descriptive name
2. **Goal**: What does this epic achieve?
3. **Core Features**: 3-5 key features/stories

### Step 3: Create Epic Folder

Create `epics/NN-[epic-name]/` with:

**EPIC.md**:
```markdown
# Epic: [Epic Name]

## Overview

**ID**: [NN]
**Status**: TODO
**Priority**: [P0/P1/P2]
**Estimated Effort**: [X days]

## Goal

[One paragraph describing what this epic achieves]

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## User Stories

### Story 1: [Title]

**As a** [user type]
**I want to** [action]
**So that** [benefit]
```

**tasks.md**:
```markdown
# Tasks: [Epic Name]

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | [N] |
| Completed | 0 |
| Progress | 0% |

## Phase 1: [Phase Name]

| ID | Task | Status | Est. | Notes |
|----|------|--------|------|-------|
| 1.1 | [Task] | TODO | [Xh] | |
```

**notes.md**:
```markdown
# Development Notes: [Epic Name]

## Quick Reference

**Current Focus**: Not started
**Last Updated**: [Date]

## Session Log

(No sessions yet)
```

### Step 4: Update ROADMAP.md

Add new Epic to the release plan table.

### Step 5: Output Summary

```
## Epic Created

**Epic**: [NN] - [Name]
**Location**: epics/NN-[name]/
**Tasks**: [N] tasks estimated

Next: Use `/project:next` to start working on this epic.
```

---

## Mode 2: Full Project Initialization (default)

Initialize a new project from the Solo Agile Template.

### Step 1: Gather Project Information

Ask for (if not in $ARGUMENTS):

**Required**:
1. **Project Name**: What is the project called?
2. **One-Line Description**: What does this project do?
3. **Target Users**: Who will use this product?
4. **Core Problem**: What problem does it solve?

**Optional**:
5. **Database Choice**: PostgreSQL (default) / SQLite / Other?
6. **Authentication**: Yes/No?
7. **MVP Features**: 3-5 core features
8. **Timeline**: Target date for MVP?

### Step 2: Initialize Documents

#### 2.1 CLAUDE.md

Update Quick Context section with project description.

#### 2.2 ROADMAP.md

Fill in:
- Vision statement
- Target Users
- v0.1 MVP with Epics

#### 2.3 docs/ARCHITECTURE.md (System Design)

**IMPORTANT**: Design the system architecture based on user requirements.

Update `docs/ARCHITECTURE.md` with project-specific architecture:

**System Context**: Update the mermaid diagram to reflect:
- External systems the project integrates with
- User types and their access patterns
- Third-party APIs (payment, auth, notifications, etc.)

**High-Level Architecture**: Customize based on features:
- If auth needed → Add Auth module
- If payments → Add Payment module  
- If notifications → Add Notification service
- If file uploads → Add Storage service

**Module Registry**: Add new modules based on MVP features:
```markdown
| Module | Location | Responsibility | Status |
|--------|----------|----------------|--------|
| core | `src/modules/core` | Shared primitives | Planned |
| agent | `src/modules/agent` | Claude Agent SDK | Stable |
| chat | `src/modules/chat` | Chat API | Stable |
| [feature] | `src/modules/[feature]` | [Description] | Planned |
```

**Data Flow**: Design data models and flows:
- Core entities (User, [Domain entities])
- Key relationships
- State transitions

**API Design**: Outline main endpoints:
```markdown
| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/chat/message | POST | Send message |
| /api/[feature]/... | ... | ... |
```

**Security Considerations**: Add project-specific security needs:
- Authentication method (JWT, OAuth, etc.)
- Authorization rules
- Data protection requirements

#### 2.4 docs/DOMAIN.md

Fill in based on user's problem domain:
- Business overview
- Core domain concepts (entities, value objects)
- Key business rules
- Domain glossary

#### 2.5 Create First Epic

Create `epics/01-[first-feature]/` using the Epic creation process above.

#### 2.6 STATUS.md

Initialize with:
```markdown
# Current Development Status

> Last Updated: [TODAY] by Claude Session #1

## Current Focus

**Epic**: 01 - [First Feature Name]
**Task**: Project setup
**Started**: [TODAY]

### What's Done This Session

- [x] Project initialized from template
- [x] Architecture designed

### Next Up

1. [First task from Epic 01]
```

#### 2.7 Configuration Files

- `backend/.env`: Update APP_NAME
- `frontend/index.html`: Update title
- `frontend/src/pages/HomePage.tsx`: Update welcome message

### Step 3: Output Summary

```
## Project Initialization Complete

**Project**: [Name]
**Description**: [One-liner]

### Documents Updated
- [x] CLAUDE.md - Project context
- [x] ROADMAP.md - Release plan with epics
- [x] docs/ARCHITECTURE.md - System architecture design
- [x] docs/DOMAIN.md - Domain model and business rules
- [x] STATUS.md - Initial status
- [x] epics/01-[name]/ - First epic created
- [x] Configuration files

### Architecture Highlights

- **Modules**: [List of planned modules]
- **Key Integrations**: [External services]
- **Data Entities**: [Core domain entities]

### Next Steps

1. Review architecture in `docs/ARCHITECTURE.md`
2. Run `make install` to install dependencies
3. Run `make dev` to start development
4. Use `/project:context` to load context
5. Use `/project:next` to get first task
```

---

## Important Notes

- Always confirm with user before making changes
- Create realistic task estimates
- Break features into small, achievable epics
- Focus on getting to a working MVP quickly

$ARGUMENTS
