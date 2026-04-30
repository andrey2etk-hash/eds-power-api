-- Stage 8A.1 — active migration after local baseline replay (see audit STAGE_8A_1).
-- Ordering: MUST run strictly after `20260429110000_remote_legacy_baseline.sql`.
--
-- Stage 8A.0.1 — root migration governance: system table, product on row.
-- TABLE = SYSTEM (neutral name). ROW = PRODUCT via product_type.
-- snapshot_version = KZO_MVP_SNAPSHOT_V1 remains the frozen contract id (Stage 7B); not a table name.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS public.calculation_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_type TEXT NOT NULL,
    snapshot_version TEXT NOT NULL CONSTRAINT calc_snap_v1_ver CHECK (snapshot_version = 'KZO_MVP_SNAPSHOT_V1'),
    run_status TEXT NOT NULL CONSTRAINT calc_snap_v1_rs CHECK (run_status IN ('SUCCESS', 'FAILED')),
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
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT calc_snap_product_kzo_mvp CHECK (
        product_type = 'KZO'
    )
);

COMMENT ON TABLE public.calculation_snapshots IS
    'EDS Power calculation snapshot store (snapshots domain). KZO is first consumer via product_type row discriminator; KZO_MVP_SNAPSHOT_V1 = contract id, not ownership.';

COMMENT ON COLUMN public.calculation_snapshots.product_type IS
    'Product line discriminator (e.g. KZO). Expand via new migration when new consumers ship.';
