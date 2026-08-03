# LUCY STANDALONE V2
## Living Project Handoff
Date: 2026-08-03

---

# Mission

Lucy is a deterministic local engineering assistant.

Truth before intelligence.
Evidence before assumptions.
Registry before subprocess.
Code before prompts.

Lucy should execute engineering work predictably, locally, and transparently.

No hidden magic.

---

# Current Milestone

## M1 — Dispatcher v1

STATUS

🟡 In Progress

Goal:

Build a production-quality dispatcher capable of routing every command through deterministic handlers while remaining fully testable.

Freeze this milestone before adding new capabilities.

---

# Definition of Done

Required:

✓ pytest passes

✓ Dispatcher coverage >90%

✓ Registry is single source of truth

✓ deterministic commands never bypass Registry

✓ cwd updates correctly

✓ regression tests exist

✓ subprocess only used for approved commands

✓ feature branch merged

Only then freeze Dispatcher v1.

---

# Verified Evidence

Current verified state:

✓ Lucy CLI launches

✓ Dispatcher exists

✓ Registry exists

✓ Filesystem handlers exist

✓ subprocess wrapper exists

✓ plugin registration exists

Observed bug:

Dispatcher attempted to execute

cd sub

through subprocess.

Result:

FileNotFoundError

Root cause:

filesystem handlers had not registered before Dispatcher dispatch().

Fix direction:

Import handler modules before dispatch begins and make Registry authoritative.

---

# Engineering Rules

1.
Registry owns routing.

2.
Dispatcher never knows command implementations.

3.
Deterministic commands NEVER fall through to subprocess.

4.
Unknown deterministic command

↓

exit code 127

NOT subprocess.

5.
Registry configuration failures

↓

exit code 70

Lucy must stay alive.

6.
One subprocess wrapper.

Never duplicate subprocess logic.

7.
Everything testable.

---

# Current Architecture

Lucy CLI

↓

Dispatcher

↓

Registry

↓

Filesystem
Git
Future plugins

↓

CommandResult

↓

Audit

Only non-deterministic commands may reach subprocess.

---

# Current Coverage

Previously observed

Dispatcher
≈69%

Repository
≈84%

Target

Dispatcher
>90%

---

# Test Loop

Until milestone complete:

Review

↓

Implement

↓

pytest

↓

Fix

↓

pytest

↓

Coverage

↓

Regression tests

↓

Commit

↓

Repeat

---

# Immediate Tasks

1.

Finish Dispatcher v1

2.

Reach >90% coverage

3.

Freeze Dispatcher

STOP

Do not build new features before freeze.

---

# Milestone Roadmap

M1

Dispatcher

M2

Filesystem Engine

M3

Git Engine

M4

Test Runner

M5

Audit Engine

M6

Planner

M7

Software Factory

---

# Software Factory Direction

Lucy follows software factory principles.

Observable

Every action measurable.

Customizable

Configuration over hardcoding.

Reusable

Drop into any repository.

Workflow

Plan

↓

Build

↓

Test

↓

Fix

↓

Review

↓

Document

↓

Commit

↓

Repeat

Validation gates between every stage.

Models propose work.

Code validates work.

---

# Lessons Learned

Do not redesign.

Smallest correct change.

Evidence over opinions.

Regression test every bug.

Freeze milestones.

Less is more.

---

# Next Coding Prompt

Project

Lucy Standalone v2

Branch

feature/dispatcher-v1

Mission

Complete Dispatcher v1.

Rules

• Smallest correct change.

• No redesign.

• Registry is single source of truth.

• Deterministic commands never use subprocess.

• One subprocess wrapper.

• Add regression test for every fix.

Loop

Review

↓

Implement

↓

pytest

↓

Fix

↓

pytest

↓

Coverage

↓

Commit

↓

Repeat

Done when

✓ pytest passes

✓ Dispatcher >90%

✓ feature frozen

Return only

• Commit SHA

• Pytest summary

• Coverage

• Files changed

• Remaining issues

---

# North Star

Lucy should become a local engineering operating system.

Deterministic.

Observable.

Auditable.

Extensible.

Simple.

The codebase should become easier to understand after every milestone, not harder. Add this to repository
