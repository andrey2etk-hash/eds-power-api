-- SUPERSEDED by Stage 8A.0.1 — do not run as an additional migration.
-- Canonical DDL (held): ../_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql

-- Stage 8A — insert-only persistence for frozen KZO_MVP_SNAPSHOT_V1
-- Run in Supabase SQL editor or via `supabase db push`.
-- Governance: INSERT only from API service role — no KPI/BOM decomposition at this stage.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS public.kzo_mvp_snapshots_v1 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_version TEXT NOT NULL CONSTRAINT kzo_snap_v1_ver CHECK (snapshot_version = 'KZO_MVP_SNAPSHOT_V1'),
    run_status TEXT NOT NULL CONSTRAINT kzo_snap_v1_rs CHECK (run_status IN ('SUCCESS', 'FAILED')),
    timestamp_basis TIMESTAMPTZ NOT NULL,
    logic_version TEXT,
    request_metadata JSONB,
    normalized_input JSONB,
    structural_composition_summary JSONB,
    physical_summary JSONB,
    physical_topology_summary JSONB,
    engineering_class_summary JSONB,
    engineering_burden_summary JSONB,
    failure JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.kzo_mvp_snapshots_v1 IS 'Stage 8A singleton table: frozen KZO_MVP_SNAPSHOT_V1 payloads; append-only by design.';
