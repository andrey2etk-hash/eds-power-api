-- =============================================================================
-- Stage 8A.0.6 — Remote legacy baseline (FACTUAL DDL from pg_dump via pooler).
-- Source: remote_schema.sql (repo root).
-- Sanitized: removed \\restrict / \\unrestrict markers; CREATE SCHEMA IF NOT EXISTS.
-- Governance: schema-only migration · no guessed DDL · no calculation_snapshots in this file
--   (remains supabase/migrations/_pending_after_remote_baseline/).
-- Ordering: 20260429110000 < 20260429120000
-- STRICT: Do not prod db_push from TASK framing; replay verify locally (Stage 8A.0.4).
-- =============================================================================

--
-- PostgreSQL database dump
--

-- (pg_dump \\restrict marker removed — not valid migration SQL.)

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA IF NOT EXISTS public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: get_bom_tree(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_bom_tree(root_id text) RETURNS TABLE(level integer, parent_id text, child_id text, child_name text, item_type text, qty_per_parent numeric, qty_total numeric, status text, is_standard boolean, replaced_by_id text, has_active_ncr text, manufacture text, transfer_to text, extra_processing text, coating text, color text, material text, size_a numeric, size_b numeric, blank_length numeric, mass_each numeric, area_each numeric, path text)
    LANGUAGE sql
    AS $$
with recursive bom_tree as (
  select
    bl.parent_id,
    bl.child_id,
    1 as level,
    bl.quantity as qty_per_parent,
    bl.quantity as qty_total,
    (bl.parent_id || ' > ' || bl.child_id) as path
  from public.bom_links bl
  where bl.parent_id = root_id
    and bl.is_active = true

  union all

  select
    bl.parent_id,
    bl.child_id,
    bt.level + 1 as level,
    bl.quantity as qty_per_parent,
    bt.qty_total * bl.quantity as qty_total,
    (bt.path || ' > ' || bl.child_id) as path
  from public.bom_links bl
  join bom_tree bt
    on bl.parent_id = bt.child_id
  where bl.is_active = true
)
select
  bt.level,
  bt.parent_id,
  bt.child_id,
  o.name as child_name,
  o.item_type,
  bt.qty_per_parent,
  bt.qty_total,
  o.status,
  o.is_standard,
  o.replaced_by_id,
  case
    when exists (
      select 1
      from public.ncr n
      where n.object_id = bt.child_id
        and n.ncr_status in ('🔴 ВІДКРИТО', '🟡 В РОБОТІ')
    ) then 'так'
    else 'ні'
  end as has_active_ncr,
  o.manufacture,
  o.transfer_to,
  o.extra_processing,
  o.coating,
  o.color,
  o.material,
  o.size_a,
  o.size_b,
  o.blank_length,
  o.mass_each,
  o.area_each,
  bt.path
from bom_tree bt
left join public.objects o
  on o.id = bt.child_id
order by bt.path;
$$;


--
-- Name: get_leaf_summary(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_leaf_summary(root_id text) RETURNS TABLE(id text, name text, item_type text, qty_total numeric, status text, is_standard boolean, replaced_by_id text, has_active_ncr text, manufacture text, transfer_to text, extra_processing text, coating text, color text, material text, size_a numeric, size_b numeric, blank_length numeric, mass_each numeric, area_each numeric)
    LANGUAGE sql
    AS $$
with recursive bom_tree as (
  select
    bl.parent_id,
    bl.child_id,
    1 as level,
    bl.quantity as qty_per_parent,
    bl.quantity as qty_total
  from public.bom_links bl
  where bl.parent_id = root_id
    and bl.is_active = true

  union all

  select
    bl.parent_id,
    bl.child_id,
    bt.level + 1 as level,
    bl.quantity as qty_per_parent,
    bt.qty_total * bl.quantity as qty_total
  from public.bom_links bl
  join bom_tree bt
    on bl.parent_id = bt.child_id
  where bl.is_active = true
),

leaf_items as (
  select
    bt.child_id,
    bt.qty_total
  from bom_tree bt
  where not exists (
    select 1
    from public.bom_links bl2
    where bl2.parent_id = bt.child_id
      and bl2.is_active = true
  )
)

select
  li.child_id as id,
  o.name,
  o.item_type,
  sum(li.qty_total) as qty_total,
  o.status,
  o.is_standard,
  o.replaced_by_id,
  case
    when exists (
      select 1
      from public.ncr n
      where n.object_id = li.child_id
        and n.ncr_status in ('🔴 ВІДКРИТО', '🟡 В РОБОТІ')
    ) then 'так'
    else 'ні'
  end as has_active_ncr,
  o.manufacture,
  o.transfer_to,
  o.extra_processing,
  o.coating,
  o.color,
  o.material,
  o.size_a,
  o.size_b,
  o.blank_length,
  o.mass_each,
  o.area_each
from leaf_items li
left join public.objects o
  on o.id = li.child_id
group by
  li.child_id,
  o.name,
  o.item_type,
  o.status,
  o.is_standard,
  o.replaced_by_id,
  o.manufacture,
  o.transfer_to,
  o.extra_processing,
  o.coating,
  o.color,
  o.material,
  o.size_a,
  o.size_b,
  o.blank_length,
  o.mass_each,
  o.area_each
order by li.child_id;
$$;


--
-- Name: set_updated_at(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.set_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
  new.updated_at = now();
  return new;
end;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bom_links; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bom_links (
    id bigint NOT NULL,
    parent_id text NOT NULL,
    child_id text NOT NULL,
    quantity numeric NOT NULL,
    entry_note text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT bom_links_quantity_check CHECK ((quantity > (0)::numeric))
);


--
-- Name: bom_links_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bom_links_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bom_links_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bom_links_id_seq OWNED BY public.bom_links.id;


--
-- Name: ncr; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ncr (
    id bigint NOT NULL,
    ncr_code text,
    issue_date date,
    object_id text NOT NULL,
    object_name text,
    issue_description text NOT NULL,
    issue_type text,
    detected_at text,
    project_object text,
    reported_by text,
    ncr_status text NOT NULL,
    resolution text,
    new_object_id text,
    note text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ncr_ncr_status_check CHECK ((ncr_status = ANY (ARRAY['🔴 ВІДКРИТО'::text, '🟡 В РОБОТІ'::text, '🟢 ЗАКРИТО'::text])))
);


--
-- Name: ncr_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ncr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ncr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ncr_id_seq OWNED BY public.ncr.id;


--
-- Name: objects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.objects (
    id text NOT NULL,
    name text NOT NULL,
    item_type text NOT NULL,
    status text NOT NULL,
    replaced_by_id text,
    is_standard boolean DEFAULT false NOT NULL,
    description text,
    manufacture text,
    transfer_to text,
    extra_processing text,
    coating text,
    color text,
    material text,
    size_a numeric,
    size_b numeric,
    blank_length numeric,
    mass_each numeric,
    area_each numeric,
    note text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT objects_item_type_check CHECK ((item_type = ANY (ARRAY['Деталь'::text, 'Вузол'::text, 'Виріб'::text]))),
    CONSTRAINT objects_status_check CHECK ((status = ANY (ARRAY['🟢 АКТИВ'::text, '🔴 ЗАБОРОНЕНО'::text, '🟡 АРХІВ'::text])))
);


--
-- Name: production_status; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.production_status (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    root_id text,
    item_id text,
    stage text,
    planned_qty numeric,
    done_qty numeric DEFAULT 0,
    status text DEFAULT 'planned'::text,
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: v_bom_tree; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_bom_tree AS
 WITH RECURSIVE bom AS (
         SELECT bl.parent_id AS root_id,
            bl.parent_id,
            bl.child_id,
            1 AS level,
            bl.quantity AS qty_on_level,
            bl.quantity AS qty_total,
            bl.entry_note,
            bl.child_id AS path
           FROM public.bom_links bl
          WHERE (bl.is_active = true)
        UNION ALL
         SELECT bom_1.root_id,
            bl.parent_id,
            bl.child_id,
            (bom_1.level + 1) AS level,
            bl.quantity AS qty_on_level,
            (bom_1.qty_total * bl.quantity) AS qty_total,
            bl.entry_note,
            ((bom_1.path || ' -> '::text) || bl.child_id) AS path
           FROM (bom bom_1
             JOIN public.bom_links bl ON ((bl.parent_id = bom_1.child_id)))
          WHERE (bl.is_active = true)
        )
 SELECT root_id,
    parent_id,
    child_id,
    level,
    qty_on_level,
    qty_total,
    entry_note,
    path
   FROM bom;


--
-- Name: v_assembly_composition; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_assembly_composition AS
 SELECT t.root_id,
    t.parent_id AS assembly_id,
    p.name AS assembly_name,
    t.child_id AS component_id,
    c.name AS component_name,
    c.item_type AS component_type,
    t.level,
    t.qty_on_level,
    t.qty_total,
    t.path
   FROM ((public.v_bom_tree t
     LEFT JOIN public.objects p ON ((p.id = t.parent_id)))
     LEFT JOIN public.objects c ON ((c.id = t.child_id)));


--
-- Name: v_bom_assemblies; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_bom_assemblies AS
 SELECT t.root_id,
    t.parent_id,
    t.child_id AS assembly_id,
    o.name,
    o.item_type,
    t.level,
    t.qty_on_level,
    t.qty_total,
    t.path
   FROM (public.v_bom_tree t
     LEFT JOIN public.objects o ON ((o.id = t.child_id)))
  WHERE (t.child_id IN ( SELECT DISTINCT bom_links.parent_id
           FROM public.bom_links
          WHERE (bom_links.is_active = true)));


--
-- Name: v_assembly_layers; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_assembly_layers AS
 SELECT root_id,
    assembly_id,
    name AS assembly_name,
    level,
    qty_total,
    path
   FROM public.v_bom_assemblies a;


--
-- Name: v_assembly_plan; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_assembly_plan AS
 SELECT root_id,
    assembly_id,
    assembly_name,
    max(level) AS assembly_level,
    component_id,
    component_name,
    component_type,
    qty_on_level
   FROM public.v_assembly_composition ac
  GROUP BY root_id, assembly_id, assembly_name, component_id, component_name, component_type, qty_on_level;


--
-- Name: v_bom_leaf_items; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_bom_leaf_items AS
 SELECT t.root_id,
    t.parent_id,
    t.child_id AS item_id,
    o.name,
    o.item_type,
    t.level,
    t.qty_on_level,
    t.qty_total,
    t.path
   FROM (public.v_bom_tree t
     LEFT JOIN public.objects o ON ((o.id = t.child_id)))
  WHERE (NOT (t.child_id IN ( SELECT DISTINCT bom_links.parent_id
           FROM public.bom_links
          WHERE (bom_links.is_active = true))));


--
-- Name: v_final_assembly_plan; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_final_assembly_plan AS
 SELECT root_id,
    assembly_id,
    assembly_name,
    assembly_level,
    component_id,
    component_name,
    component_type,
    qty_on_level
   FROM public.v_assembly_plan ap
  WHERE (assembly_id = root_id);


--
-- Name: v_subassembly_plan; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_subassembly_plan AS
 SELECT root_id,
    assembly_id,
    assembly_name,
    assembly_level,
    component_id,
    component_name,
    component_type,
    qty_on_level
   FROM public.v_assembly_plan ap
  WHERE (assembly_id <> root_id);


--
-- Name: v_assembly_roadmap; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_assembly_roadmap AS
 SELECT l.root_id,
    'detail'::text AS step_type,
    l.level AS step_level,
    NULL::text AS assembly_id,
    NULL::text AS assembly_name,
    l.item_id AS component_id,
    l.name AS component_name,
    l.item_type AS component_type,
    l.qty_total AS qty,
    l.path
   FROM public.v_bom_leaf_items l
UNION ALL
 SELECT s.root_id,
    'subassembly'::text AS step_type,
    s.assembly_level AS step_level,
    s.assembly_id,
    s.assembly_name,
    s.component_id,
    s.component_name,
    s.component_type,
    s.qty_on_level AS qty,
    NULL::text AS path
   FROM public.v_subassembly_plan s
UNION ALL
 SELECT f.root_id,
    'final_assembly'::text AS step_type,
    f.assembly_level AS step_level,
    f.assembly_id,
    f.assembly_name,
    f.component_id,
    f.component_name,
    f.component_type,
    f.qty_on_level AS qty,
    NULL::text AS path
   FROM public.v_final_assembly_plan f;


--
-- Name: v_objects_actual; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_objects_actual AS
 SELECT o.id AS original_id,
    o.name AS original_name,
    o.item_type,
    o.replaced_by_id,
    COALESCE(o.replaced_by_id, o.id) AS actual_id,
    oa.name AS actual_name
   FROM (public.objects o
     LEFT JOIN public.objects oa ON ((oa.id = COALESCE(o.replaced_by_id, o.id))));


--
-- Name: v_bom_tree_actual; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_bom_tree_actual AS
 WITH RECURSIVE bom AS (
         SELECT bl.parent_id AS root_id,
            bl.parent_id,
            bl.child_id,
            1 AS level,
            bl.quantity AS qty_on_level,
            bl.quantity AS qty_total,
            bl.entry_note,
            bl.child_id AS path
           FROM public.bom_links bl
          WHERE (bl.is_active = true)
        UNION ALL
         SELECT bom_1.root_id,
            bl.parent_id,
            bl.child_id,
            (bom_1.level + 1) AS level,
            bl.quantity AS qty_on_level,
            (bom_1.qty_total * bl.quantity) AS qty_total,
            bl.entry_note,
            ((bom_1.path || ' -> '::text) || bl.child_id) AS path
           FROM (bom bom_1
             JOIN public.bom_links bl ON ((bl.parent_id = bom_1.child_id)))
          WHERE (bl.is_active = true)
        )
 SELECT bom.root_id,
    bom.parent_id,
    bom.child_id AS original_child_id,
    voa.actual_id AS child_id,
    voa.actual_name AS child_name,
    voa.item_type,
    bom.level,
    bom.qty_on_level,
    bom.qty_total,
    bom.entry_note,
    bom.path
   FROM (bom
     LEFT JOIN public.v_objects_actual voa ON ((voa.original_id = bom.child_id)));


--
-- Name: v_bom_leaf_items_actual; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_bom_leaf_items_actual AS
 SELECT root_id,
    parent_id,
    original_child_id,
    child_id AS item_id,
    child_name AS name,
    item_type,
    level,
    qty_on_level,
    qty_total,
    path
   FROM public.v_bom_tree_actual t
  WHERE (NOT (child_id IN ( SELECT DISTINCT bom_links.parent_id
           FROM public.bom_links
          WHERE (bom_links.is_active = true))));


--
-- Name: v_assembly_roadmap_actual; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_assembly_roadmap_actual AS
 SELECT l.root_id,
    'detail'::text AS step_type,
    l.level AS step_level,
    NULL::text AS assembly_id,
    NULL::text AS assembly_name,
    l.item_id AS component_id,
    l.name AS component_name,
    l.item_type AS component_type,
    l.qty_total AS qty,
    l.path
   FROM public.v_bom_leaf_items_actual l
UNION ALL
 SELECT t.root_id,
    'subassembly'::text AS step_type,
    t.level AS step_level,
    t.parent_id AS assembly_id,
    p.name AS assembly_name,
    t.child_id AS component_id,
    t.child_name AS component_name,
    t.item_type AS component_type,
    t.qty_on_level AS qty,
    t.path
   FROM (public.v_bom_tree_actual t
     LEFT JOIN public.objects p ON ((p.id = t.parent_id)))
  WHERE ((t.parent_id <> t.root_id) AND (t.parent_id IN ( SELECT DISTINCT bom_links.parent_id
           FROM public.bom_links
          WHERE (bom_links.is_active = true))))
UNION ALL
 SELECT t.root_id,
    'final_assembly'::text AS step_type,
    t.level AS step_level,
    t.parent_id AS assembly_id,
    p.name AS assembly_name,
    t.child_id AS component_id,
    t.child_name AS component_name,
    t.item_type AS component_type,
    t.qty_on_level AS qty,
    t.path
   FROM (public.v_bom_tree_actual t
     LEFT JOIN public.objects p ON ((p.id = t.parent_id)))
  WHERE (t.parent_id = t.root_id);


--
-- Name: v_assembly_sequence; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_assembly_sequence AS
 SELECT DISTINCT v_subassembly_plan.root_id,
    'subassembly'::text AS assembly_kind,
    v_subassembly_plan.assembly_id,
    v_subassembly_plan.assembly_name,
    v_subassembly_plan.assembly_level
   FROM public.v_subassembly_plan
UNION
 SELECT DISTINCT v_final_assembly_plan.root_id,
    'final'::text AS assembly_kind,
    v_final_assembly_plan.assembly_id,
    v_final_assembly_plan.assembly_name,
    v_final_assembly_plan.assembly_level
   FROM public.v_final_assembly_plan;


--
-- Name: v_bom_expanded; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_bom_expanded AS
 WITH RECURSIVE bom AS (
         SELECT bl.parent_id AS root_id,
            bl.child_id AS item_id,
            1 AS level,
            bl.quantity AS qty_path
           FROM public.bom_links bl
          WHERE (bl.is_active = true)
        UNION ALL
         SELECT bom_1.root_id,
            bl.child_id AS item_id,
            (bom_1.level + 1) AS level,
            (bom_1.qty_path * bl.quantity) AS qty_path
           FROM (bom bom_1
             JOIN public.bom_links bl ON ((bl.parent_id = bom_1.item_id)))
          WHERE (bl.is_active = true)
        )
 SELECT root_id,
    item_id,
    min(level) AS first_level,
    sum(qty_path) AS total_qty
   FROM bom
  GROUP BY root_id, item_id;


--
-- Name: v_stage_readiness; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_stage_readiness AS
 WITH live AS (
         SELECT ps.id,
            ps.root_id,
            ps.item_id,
            ps.stage,
            ps.planned_qty,
            ps.done_qty,
            ps.status,
            ps.updated_at,
                CASE
                    WHEN (COALESCE(ps.done_qty, (0)::numeric) <= (0)::numeric) THEN 'planned'::text
                    WHEN (COALESCE(ps.done_qty, (0)::numeric) < ps.planned_qty) THEN 'in_progress'::text
                    WHEN (COALESCE(ps.done_qty, (0)::numeric) >= ps.planned_qty) THEN 'done'::text
                    ELSE ps.status
                END AS live_status,
                CASE ps.stage
                    WHEN 'ЛОМ'::text THEN 1
                    WHEN 'звар.'::text THEN 2
                    WHEN 'фарб.'::text THEN 3
                    WHEN 'збір.'::text THEN 4
                    ELSE 99
                END AS stage_order
           FROM public.production_status ps
        )
 SELECT cur.root_id,
    cur.item_id,
    cur.stage,
    cur.planned_qty,
    cur.done_qty,
    cur.status,
    cur.live_status,
    cur.stage_order,
    prev.stage AS prev_stage,
    prev.done_qty AS prev_done_qty,
    prev.planned_qty AS prev_planned_qty,
    prev.live_status AS prev_live_status,
        CASE
            WHEN (cur.stage_order = 1) THEN 'ready'::text
            WHEN (COALESCE(prev.done_qty, (0)::numeric) >= prev.planned_qty) THEN 'ready'::text
            ELSE 'blocked'::text
        END AS readiness
   FROM (live cur
     LEFT JOIN live prev ON (((prev.root_id = cur.root_id) AND (prev.item_id = cur.item_id) AND (prev.stage_order = (cur.stage_order - 1)))));


--
-- Name: v_ready_to_start; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_ready_to_start AS
 SELECT root_id,
    item_id,
    stage,
    planned_qty,
    done_qty,
    status,
    live_status,
    stage_order
   FROM public.v_stage_readiness
  WHERE ((readiness = 'ready'::text) AND (live_status <> 'done'::text));


--
-- Name: v_dispatch_queue; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_dispatch_queue AS
 SELECT r.root_id,
    r.item_id,
    o.name,
    r.stage,
    r.planned_qty,
    r.done_qty,
    r.live_status,
    r.stage_order
   FROM (public.v_ready_to_start r
     JOIN public.objects o ON ((o.id = r.item_id)));


--
-- Name: v_object_progress; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_object_progress AS
 SELECT root_id,
    count(*) AS total_tasks,
    count(*) FILTER (WHERE ((readiness = 'ready'::text) AND (live_status <> 'done'::text))) AS ready_tasks,
    count(*) FILTER (WHERE (readiness = 'blocked'::text)) AS blocked_tasks,
    count(*) FILTER (WHERE (live_status = 'done'::text)) AS done_tasks
   FROM public.v_stage_readiness
  GROUP BY root_id;


--
-- Name: v_production_items; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_production_items AS
 SELECT b.root_id,
    o.id AS item_id,
    o.name,
    o.item_type,
    o.status,
    o.is_standard,
    o.manufacture,
    o.transfer_to,
    o.extra_processing,
    o.coating,
    o.color,
    o.material,
    o.size_a,
    o.size_b,
    o.blank_length,
    o.mass_each,
    o.area_each,
    b.first_level,
    b.total_qty
   FROM (public.v_bom_expanded b
     JOIN public.objects o ON ((o.id = b.item_id)));


--
-- Name: v_production_status_live; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_production_status_live AS
 SELECT id,
    root_id,
    item_id,
    stage,
    planned_qty,
    done_qty,
    status,
    updated_at,
        CASE
            WHEN (COALESCE(done_qty, (0)::numeric) <= (0)::numeric) THEN 'planned'::text
            WHEN (COALESCE(done_qty, (0)::numeric) < planned_qty) THEN 'in_progress'::text
            WHEN (COALESCE(done_qty, (0)::numeric) >= planned_qty) THEN 'done'::text
            ELSE status
        END AS live_status
   FROM public.production_status ps;


--
-- Name: v_production_status_ordered; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_production_status_ordered AS
 SELECT id,
    root_id,
    item_id,
    stage,
    planned_qty,
    done_qty,
    status,
    updated_at,
        CASE stage
            WHEN 'ЛОМ'::text THEN 1
            WHEN 'звар.'::text THEN 2
            WHEN 'фарб.'::text THEN 3
            WHEN 'збір.'::text THEN 4
            ELSE 99
        END AS stage_order
   FROM public.production_status ps;


--
-- Name: v_required_items_summary; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_required_items_summary AS
 SELECT root_id,
    item_id,
    name,
    item_type,
    sum(qty_total) AS total_required_qty
   FROM public.v_bom_leaf_items
  GROUP BY root_id, item_id, name, item_type;


--
-- Name: bom_links id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bom_links ALTER COLUMN id SET DEFAULT nextval('public.bom_links_id_seq'::regclass);


--
-- Name: ncr id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ncr ALTER COLUMN id SET DEFAULT nextval('public.ncr_id_seq'::regclass);


--
-- Name: bom_links bom_links_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bom_links
    ADD CONSTRAINT bom_links_pkey PRIMARY KEY (id);


--
-- Name: bom_links bom_links_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bom_links
    ADD CONSTRAINT bom_links_unique UNIQUE (parent_id, child_id, is_active);


--
-- Name: ncr ncr_ncr_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ncr
    ADD CONSTRAINT ncr_ncr_code_key UNIQUE (ncr_code);


--
-- Name: ncr ncr_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ncr
    ADD CONSTRAINT ncr_pkey PRIMARY KEY (id);


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: production_status production_status_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.production_status
    ADD CONSTRAINT production_status_pkey PRIMARY KEY (id);


--
-- Name: production_status production_status_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.production_status
    ADD CONSTRAINT production_status_unique UNIQUE (root_id, item_id, stage);


--
-- Name: idx_bom_links_active; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bom_links_active ON public.bom_links USING btree (is_active);


--
-- Name: idx_bom_links_child; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bom_links_child ON public.bom_links USING btree (child_id);


--
-- Name: idx_bom_links_parent; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_bom_links_parent ON public.bom_links USING btree (parent_id);


--
-- Name: idx_ncr_object_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ncr_object_id ON public.ncr USING btree (object_id);


--
-- Name: idx_ncr_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ncr_status ON public.ncr USING btree (ncr_status);


--
-- Name: idx_objects_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_objects_status ON public.objects USING btree (status);


--
-- Name: idx_objects_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_objects_type ON public.objects USING btree (item_type);


--
-- Name: bom_links trg_bom_links_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_bom_links_updated_at BEFORE UPDATE ON public.bom_links FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: ncr trg_ncr_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_ncr_updated_at BEFORE UPDATE ON public.ncr FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: objects trg_objects_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_objects_updated_at BEFORE UPDATE ON public.objects FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: bom_links bom_links_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bom_links
    ADD CONSTRAINT bom_links_child_id_fkey FOREIGN KEY (child_id) REFERENCES public.objects(id) ON DELETE RESTRICT;


--
-- Name: bom_links bom_links_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bom_links
    ADD CONSTRAINT bom_links_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.objects(id) ON DELETE CASCADE;


--
-- Name: ncr ncr_new_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ncr
    ADD CONSTRAINT ncr_new_object_id_fkey FOREIGN KEY (new_object_id) REFERENCES public.objects(id);


--
-- Name: ncr ncr_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ncr
    ADD CONSTRAINT ncr_object_id_fkey FOREIGN KEY (object_id) REFERENCES public.objects(id) ON DELETE RESTRICT;


--
-- Name: objects objects_replaced_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_replaced_by_id_fkey FOREIGN KEY (replaced_by_id) REFERENCES public.objects(id);


--
-- PostgreSQL database dump complete
--

-- (pg_dump \\unrestrict marker removed — not valid migration SQL.)
