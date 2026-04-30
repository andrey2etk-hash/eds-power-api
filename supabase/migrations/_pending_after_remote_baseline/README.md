# Pending migrations folder (future holds)

**Stage 8A.1:** canonical **`calculation_snapshots`** migration was **promoted** to **`supabase/migrations/20260429120000_calculation_snapshots_v1.sql`**. This directory no longer holds that file.

## Purpose

Reserve **`_pending_after_remote_baseline/`** for DDL that **must apply only after** a verified legacy **`public`** baseline migration sequence — same governance pattern as **8A.0.2** (additive, no destructive remote mutations from undocumented TASK).

## Restore workflow (when adding a new held file)

1. Land authoritative baseline migrations in **`supabase/migrations/`** with timestamps strictly **before** the held migration.
2. Move or commit the held SQL into **`migrations/`** with a timestamp **after** baseline files.
3. Verify with **`supabase db reset`** (local/disposable) before any production-linked apply.
