docs/handoffs/2026-08-03-dispatcher-v1-living-handoff.md:
# Lucy Standalone V2 — Living Engineering Handoff
Date: 2026-08-03

## Project Goal

Ship Lucy Standalone V2 as a real, runnable product.

Priority:

1. Product works.
2. Tests pass.
3. Public release.
4. Documentation.
5. Future features.

No scope creep.

---

# Repository

Branch:
feature/dispatcher-v1

Latest verified pushed commit:
7f0e3c3

Working tree:
CLEAN

Git status:
Working tree clean.
Branch synchronized with origin.

---

# Verified Engineering Timeline

Initial Dispatcher implementation:
0b89b1a

Dispatcher fixes:
6232352
- import filesystem handlers
- import git handlers
- regression test preventing cd subprocess fallback

8bdc9ae
- don't swallow handler exceptions
- dispatcher.run_subprocess test updates
- cd regression improvements

b6ab471
- M1 living handoff documentation

8f20e84
- Dispatcher checkpoint

7f0e3c3
- removed generated artifacts
- repository cleanup

---

# Current Executable Evidence

pytest:

6 FAILED
3 PASSED

coverage:

TOTAL 54%

dispatcher.py 51%

filesystem.py 24%

registry.py 95%

Current failing tests:

test_dispatch_uses_registered_handler_pwd

test_dispatch_missing_deterministic_command_is_blocked

test_dispatch_non_deterministic_falls_to_subprocess

test_registry_lookup_exception_returns_internal_error

test_cd_never_uses_subprocess

test_cd_does_not_use_subprocess

---

# Verified Root Cause

Dispatcher expects deterministic registry metadata.

Dispatcher explicitly calls:

default_registry.lookup(...)

Current registry implementation does NOT expose:

lookup()

Dispatcher therefore intentionally returns:

Dispatcher configuration error:
registry does not expose deterministic command metadata

This is NOT a cd bug.

This is NOT a subprocess bug.

This is an API mismatch between dispatcher.py and registry.py.

Dispatcher and Registry originate from different revisions.

---

# Required Registry API

CommandRegistry must expose:

register(...)

get(...)

lookup(...)

is_deterministic(...)

lookup()

must return an object compatible with Dispatcher expectations:

handler

deterministic

Do NOT redesign Dispatcher.

Update Registry to satisfy Dispatcher.

---

# Dispatcher Rules

Deterministic commands MUST NEVER invoke subprocess.

Non-deterministic commands MAY invoke subprocess.

Dispatcher must remain frozen unless executable evidence proves Dispatcher incorrect.

---

# Current Release Status

Dispatcher V1

NOT RELEASED

Reason:

pytest failing

coverage below target

registry API incomplete

---

# Do NOT Do

Do NOT weaken tests.

Do NOT disable tests.

Do NOT bypass Dispatcher.

Do NOT remove deterministic dispatch.

Do NOT fabricate coverage.

Do NOT fabricate commits.

Do NOT fabricate test results.

---

# Engineering Process

Loop:

Inspect

Identify smallest blocker

Fix blocker only

pytest

coverage

commit

repeat

No multiple milestone work.

One blocker at a time.

---

# Immediate Task

Bring registry.py into conformance with dispatcher.py.

Nothing else.

---

# Verification Commands

pytest -q

coverage run -m pytest

coverage report -m

git status

git log --oneline -5

---

# Definition of Done

Dispatcher V1 complete only when:

All tests green

Dispatcher deterministic dispatch verified

lookup() implemented

No subprocess for deterministic commands

Coverage verified from executable runs

Working tree clean

Commit pushed

GitHub synchronized

---

# Next Milestone

Only after Dispatcher V1 passes:

M2 Filesystem Engine

Not before.

---

# Engineering Philosophy

Evidence over assumptions.

Executable proof over documentation.

Smallest correct fix.

Ship before expanding scope.

One product.

One roadmap.

One public release.
This captures the current verified state, the ^o
out

