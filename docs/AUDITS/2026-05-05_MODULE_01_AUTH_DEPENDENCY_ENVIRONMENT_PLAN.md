# MODULE 01 AUTH DEPENDENCY AND ENVIRONMENT PLAN

## Status
DOC ONLY / DEPENDENCY AND ENVIRONMENT PLANNING / NO CHANGES

## Purpose
Define dependencies and environment variables required for Module 01 authorization API implementation.

## Source Findings
Reference:
- API Auth Slice 1A Repo Inspection Result
- API Auth Endpoint Implementation Slice Plan
- API Auth Endpoint Data Contract Plan

Key findings:
- password hashing libraries are not declared
- HMAC/SHA256 can use Python standard library
- existing server-side Supabase env pattern is already present
- Render env must store secrets, not repository files

## Dependency Requirements

### Password Hashing

Required capability:
- verify stored `password_hash` for user login
- support `password_algorithm` values:
  - ARGON2ID
  - BCRYPT

Options:

#### Option A — argon2-cffi + bcrypt
Pros:
- direct support for both algorithms
- clear implementation

Cons:
- two libraries

#### Option B — passlib[bcrypt] + argon2-cffi
Pros:
- passlib can simplify bcrypt handling
- argon2-cffi handles Argon2id

Cons:
- more abstraction
- still needs careful version compatibility

Recommended for MVP:
- add `bcrypt` for BCRYPT verification
- add `argon2-cffi` for ARGON2ID verification

No dependency installation in this task.

## Proposed requirements.txt Additions

Planned only, not applied in this task:
- bcrypt
- argon2-cffi

Decision for Gemini:
Should passlib be included, or keep direct `bcrypt` + `argon2-cffi` only?

## Session Token Hashing

Use standard library:
- hmac
- hashlib
- secrets

No external dependency required.

Recommended:
- generate raw session token with `secrets.token_urlsafe` or `secrets.token_bytes`
- hash session token using `HMAC_SHA256` with server-side secret

## Environment Variables

Existing:
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY

Planned new env vars:

### EDS_SESSION_HMAC_SECRET
Purpose:
Secret key for HMAC_SHA256 hashing of opaque session tokens.

Rules:
- required in Render environment
- required locally for auth tests if session hashing is tested
- must never be committed
- must never be printed
- must not be exposed to GAS

### AUTH_SESSION_TTL_HOURS
Purpose:
Session expiration policy.

Recommended MVP value:
- 12

Rules:
- parse as positive integer
- default may be 12 only if explicitly approved
- invalid value should fail-safe

### API_VERSION
Purpose:
Response metadata version.

Recommended:
- keep existing API version pattern if already present
- otherwise define `API_VERSION = v1` or `0.1.0` consistently

Decision needed:
Should API_VERSION be an env var or code constant?

## .env.example Policy

Future `.env.example` may list names only, never values:
- SUPABASE_URL=
- SUPABASE_SERVICE_ROLE_KEY=
- EDS_SESSION_HMAC_SECRET=
- AUTH_SESSION_TTL_HOURS=12
- API_VERSION=v1

No real secrets.
No `.env` commit.

## Render Environment Plan

Future operator action:
- add `EDS_SESSION_HMAC_SECRET` in Render dashboard
- add `AUTH_SESSION_TTL_HOURS` in Render dashboard
- optionally add `API_VERSION`
- keep `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` unchanged

Do not perform Render changes in this task.

## Local Development Policy

Local `.env` may exist but must not be committed.

If local auth tests require env:
- use local safe dummy values
- never use production secrets in tests
- never print secret values

## Secret Generation Doctrine

`EDS_SESSION_HMAC_SECRET` should be:
- high entropy
- generated outside repository
- at least 32 bytes equivalent
- not derived from password/email/project name

Example generation method may be documented without printing actual secret:
- Python `secrets.token_urlsafe(32)`
- OpenSSL random command

No generated secret in docs.

## Fail-Safe Behavior

If required auth env var is missing:
- auth endpoints should fail closed
- return `AUTH_INTERNAL_ERROR` or service unavailable style response
- do not create sessions
- do not accept login

If password hashing dependency missing:
- implementation must stop
- do not fallback to insecure plain comparison

## Dependency Installation Boundary

This plan does not authorize:
- editing `requirements.txt`
- installing packages
- changing Render env
- editing `.env.example`
- writing code

These actions require separate approved implementation/prep task.

## Recommended Future Tasks

After Gemini PASS:
1. Auth Dependency/Env File Update Task
   - update `requirements.txt`
   - update `.env.example` with names only
   - no code
   - no secrets

2. Auth Dependency Smoke / Import Check
   - verify imports locally
   - no DB writes
   - no secrets printed

3. Test User Provisioning Plan
   - plan safe test user with corporate-style dummy email
   - no real password in docs

4. API Auth Implementation Slice 1B
   - only after dependencies and env are ready

## Open Questions For Gemini

1. Should requirements add direct `bcrypt` + `argon2-cffi`, or use `passlib`?
2. Should `EDS_SESSION_HMAC_SECRET` be mandatory with no default?
3. Should `AUTH_SESSION_TTL_HOURS` default to 12 if missing, or fail closed?
4. Should `API_VERSION` be env var or code constant?
5. Is `.env.example` update acceptable as a separate non-secret prep task?
6. Should dependency import check happen before API code?
7. Should test user provisioning plan happen before or after dependency/env update?

## Boundary

This document does not authorize:
- code changes
- requirements edits
- dependency installation
- Render env changes
- SQL
- DB writes
- secrets

## Next Allowed Step

Gemini audit of Auth Dependency and Environment Plan.

If PASS:
Create Auth Dependency/Env File Update Task.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- use direct `bcrypt` + `argon2-cffi`
- do not use `passlib` for MVP
- `EDS_SESSION_HMAC_SECRET` is mandatory with no default
- `AUTH_SESSION_TTL_HOURS` is mandatory / fail closed
- `API_VERSION` should be code constant, not env var
- `.env.example` and `requirements.txt` update is allowed as separate prep task
- dependency import check is required before API code
- test user provisioning should happen after dependency/env update
- no required blocking fixes
- next allowed step: Auth Dependency & Env File Update Task
