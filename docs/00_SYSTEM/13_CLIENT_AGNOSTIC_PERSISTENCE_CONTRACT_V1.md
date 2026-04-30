# Client-Agnostic Persistence Contract V1

## Status

**Frozen governance** for **Stage 8B** (**IDEA-0023**).  
Applies to **all** first-party clients (GAS, Web, Mobile, agents, future adapters).

## 1. Canonical flow

```text
Any Client
  → POST /api/calc/prepare_calculation
  → build / verify snapshot object (e.g. KZO_MVP_SNAPSHOT_V1 per Stage 7B)
  → POST /api/kzo/save_snapshot
  → receive snapshot_id + persistence envelope
```

- **One** persistence pathway to **`public.calculation_snapshots`** for MVP KZO snapshots (Stage 8A DDL).
- Clients **never** write the database directly.

## 2. Roles

| Layer | Responsibility |
| --- | --- |
| **Client** | HTTP to API; normalized input; display **`prepare_calculation`** + **`save_snapshot`** outcomes; optional **pre-flight form** checks only (no business truth). |
| **API** | Calculation truth; snapshot validation; **`save_snapshot`**; response contracts; Supabase insert (service role). |
| **Supabase** | Row storage; **no** engineering recomputation; **no** client behaviour. |

### 2.1 Google Apps Script

**Thin Client Adapter V1** — transport and UI binding only. **Not** the system orchestrator.

## 3. Client: allowed / forbidden

**Allowed**

- `UrlFetchApp` / HTTPS to API endpoints.
- Persist **only** via **`POST /api/kzo/save_snapshot`** after contract-valid body.
- Present **`snapshot_id`**, **`persistence_status`**, errors to the operator.

**Forbidden**

- Supabase REST/Postgres from Sheets or any non-API path.
- Encoding “saved” state **only** in Sheet as system record of truth.
- Client-side snapshot contract changes; branching logic that replaces API validation.

## 4. Persistence response (normative — V1)

Clients **must** tolerate additive fields; producers **must** supply the required set below when implementation is aligned (sub-TASK under **8B**).

### 4.1 Success

| Field | Type / notes |
| --- | --- |
| `status` | e.g. **`SUCCESS`** |
| `snapshot_id` | UUID string |
| `persistence_status` | e.g. **`STORED`** |
| `snapshot_version` | e.g. **`KZO_MVP_SNAPSHOT_V1`** |
| `created_at` | ISO-8601 timestamp (DB or API echo) |
| `failure` | **`null`** |

### 4.2 Failure / reject

| Field | Type / notes |
| --- | --- |
| `status` | e.g. **`FAILED`** |
| `persistence_status` | e.g. **`REJECTED`** |
| `snapshot_id` | **`null`** or absent |
| `snapshot_version` | present if body reached version check |
| `created_at` | **`null`** or absent |
| `failure` | structured object or **`error_code`** + message per existing API pattern — **one** reject envelope; document in **`04_DATA_CONTRACTS.md`** when stabilized |

**Implementation note:** Current **`POST /api/kzo/save_snapshot`** MUST be extended in a focused TASK to match this table (e.g. **`created_at`**, unified **`failure`**). Until then, this file is **normative target**; runtime may lag **one** minor API revision.

## 5. References

- **`docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`** — **IDEA-0023**
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`**
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/14_CALC_TRUTH_VS_PERSISTENCE_STAGE_8A.md`**
- **`docs/00_SYSTEM/02_GLOBAL_RULES.md`** — GAS thin client, validation layers
