# MODULE 01 AUTH DEPENDENCY IMPORT CHECK PLAN

## Status
DOC ONLY / DEPENDENCY IMPORT CHECK PLANNING / NO EXECUTION

## Purpose
Define a controlled local smoke-check procedure to verify new auth dependencies can be installed and imported before any Module 01 auth implementation.

## Scope
This plan verifies only:
- local dependency install command execution readiness
- import availability for `bcrypt` and `argon2`
- temporary smoke script creation and cleanup discipline

This plan does not authorize implementation.

## Preconditions
- `requirements.txt` already includes:
  - `bcrypt`
  - `argon2-cffi`
- `.env.example` already includes placeholder names only:
  - `EDS_SESSION_HMAC_SECRET`
  - `AUTH_SESSION_TTL_HOURS`
- no real secrets are required for this import smoke-check

## Planned Local Install Command

```bash
pip install -r requirements.txt
```

## Temporary Smoke Test Script Concept

Temporary file name:
- `tmp_auth_dependency_import_check.py`

Planned smoke script content (imports only):

```python
import bcrypt
from argon2 import PasswordHasher

print("bcrypt import: OK")
print("argon2 import: OK")
```

Planned execution command:

```bash
python tmp_auth_dependency_import_check.py
```

Cleanup rule:
- after test, delete `tmp_auth_dependency_import_check.py`

## Pass Criteria
- `pip install -r requirements.txt` completes locally
- `import bcrypt` succeeds
- `from argon2 import PasswordHasher` succeeds
- no secrets used
- no user data used
- no DB touched
- no API code changed
- no Render env changed

## Failure Criteria
- dependency install fails
- `import bcrypt` fails
- `from argon2 import PasswordHasher` fails
- version conflict appears
- temporary file is not removed

## Strict Boundary
This check does not:
- validate password logic
- create password hashing functions
- create sessions
- touch users
- touch Supabase
- touch Render
- modify API

## Safety Notes
- run locally only
- do not print or capture secret values
- do not create persistent test artifacts beyond the temporary smoke file
- if install/import fails, stop and record exact failure class for follow-up dependency resolution

## Execution Output Capture Plan
When execution is later approved, record:
- command run list
- install result summary (success/fail)
- import result summary (bcrypt/argon2)
- cleanup confirmation (`tmp_auth_dependency_import_check.py` removed)
- boundary confirmation (no code/db/render/env-secrets changes)

## Next Allowed Step
Gemini audit of Auth Dependency Import Check Plan.

If PASS:
- Local dependency import smoke test execution.
