---
description: Initialize project documents based on user requirements
---

You are helping to initialize a new project from the Solo Agile Template. 

## Step 1: Gather Project Information

Please ask the user for the following information (if not already provided in $ARGUMENTS):

### Required Information

1. **Project Name**: What is the project called?
2. **One-Line Description**: What does this project do in one sentence?
3. **Target Users**: Who will use this product?
4. **Core Problem**: What problem does it solve?

### Technical Preferences (Optional)

5. **Database Choice**: PostgreSQL (default) / SQLite / Other?
6. **Authentication**: Yes/No? (OAuth, JWT, etc.)
7. **Deployment Target**: Vercel / AWS / Cloudflare / Self-hosted?

### Scope

8. **MVP Features**: What are the 3-5 core features for MVP?
9. **Timeline**: Target date for MVP?

---

## Step 2: Initialize Documents

Once you have the information, update the following documents in order:

### 2.1 CLAUDE.md

Update the Quick Context section:
```markdown
## Quick Context

[User's one-line description]
```

Update Current Focus to first Epic.

### 2.2 ROADMAP.md

Fill in:
- Vision statement
- Target Users section
- v0.1 MVP section with Epics based on user's core features
- Non-Goals (ask user what's explicitly out of scope)

Example structure:
```markdown
## Vision

[One sentence vision based on user input]

## Target Users

- Primary: [From user input]

## Release Plan

### v0.1 - MVP (Target: [User's timeline])

| # | Epic | Status | Priority | Est. |
|---|------|--------|----------|------|
| 01 | [Feature 1] | TODO | P0 | Xd |
| 02 | [Feature 2] | TODO | P0 | Xd |
| 03 | [Feature 3] | TODO | P1 | Xd |
```

### 2.3 Create First Epic

Create `epics/01-[first-feature]/` by copying from template:

1. Copy `epics/00-template/` to `epics/01-[name]/`
2. Fill in EPIC.md with:
   - Goal from user's feature description
   - Success criteria
   - Initial user stories
3. Fill in tasks.md with initial task breakdown

### 2.4 STATUS.md

Initialize with:
```markdown
# Current Development Status

> Last Updated: [TODAY] by Claude Session #1

## Current Focus

**Epic**: 01 - [First Feature Name]
**Task**: Project setup and configuration
**Branch**: `main`
**Started**: [TODAY]

### What's Done This Session

- [x] Project initialized from template
- [ ] [First actual task]

### Next Up

1. [First task from Epic 01]
2. [Second task]
```

### 2.5 docs/knowledge/DOMAIN.md

Fill in:
- Business Overview
- Core Domain Concepts based on the product
- Key business rules

### 2.6 docs/knowledge/GLOSSARY.md

Add project-specific terms:
- Core entity names
- Status values
- Any domain-specific terminology

### 2.7 backend/.env

Update with project name:
```
APP_NAME="[Project Name]"
```

### 2.8 frontend/index.html

Update title:
```html
<title>[Project Name]</title>
```

### 2.9 frontend/src/pages/HomePage.tsx

Update welcome message with project name.

---

## Step 3: Technical Setup Recommendations

Based on user's choices, provide recommendations:

### If Authentication is needed:
- Suggest Epic for user auth
- Note dependencies to add

### If specific deployment target:
- Note any configuration changes needed
- Add to docs/operations/DEPLOY.md

---

## Step 4: Generate Initialization Summary

After updating all documents, provide a summary:

```
## Project Initialization Complete

**Project**: [Name]
**Description**: [One-liner]

### Documents Updated
- [x] CLAUDE.md - Project context
- [x] ROADMAP.md - Product roadmap with X epics
- [x] STATUS.md - Initial status
- [x] epics/01-[name]/ - First epic created
- [x] docs/knowledge/DOMAIN.md - Domain concepts
- [x] docs/knowledge/GLOSSARY.md - Terminology
- [x] Configuration files updated

### Created Epics
1. Epic 01: [Name] - [Status]
2. Epic 02: [Name] - [Status]
...

### Next Steps

1. Review generated documents and adjust as needed
2. Run `make install` to install dependencies
3. Run `make db-start` to start database
4. Run `make dev` to start development
5. Use `/project:context` to load context
6. Use `/project:next` to get first task

### Ready to Start

Your first task is: [First task from Epic 01]
```

---

## Conversation Flow Example

**User**: /project:init I want to build a habit tracking app

**Agent**: 
Great! Let me help you initialize the project. I need a few more details:

1. What would you like to call this project?
2. Who are the target users? (e.g., individuals, teams, specific demographics)
3. What are the 3-5 core features for MVP?
4. Do you need user authentication?
5. Any target launch date?

**User**: Call it "HabitFlow". Target users are individuals who want to build good habits. Core features: habit creation, daily check-ins, streak tracking, weekly summary. Yes need auth. Launch in 2 months.

**Agent**: [Proceeds to update all documents based on this information]

---

## Important Notes

- Always confirm with user before making changes
- Create realistic task estimates
- Break features into small, achievable epics
- Set up first epic to be achievable in 1-2 weeks
- Focus on getting to a working MVP quickly

$ARGUMENTS
