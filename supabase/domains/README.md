# Domain map (EDS Power bounded contexts)

These folders are **logical roots** — not Postgres schemas (`public` stays default unless an approved IDEA splits schemas). Purpose: **prevent** KZO-prefixed table sprawl across unrelated concerns.

## Suggested domains

| Domain | Intent (EDS Power-wide) |
| --- | --- |
| **`auth`** | Sessions, identities, MFA — **frozen until dedicated IDEA**. |
| **`users`** | Person / account linkage — **frozen**. |
| **`roles`** | RBAB / tenancy — **frozen**. |
| **`products`** | Product catalogs, SKU — **frozen** (no BOM seeding in MVP governance). |
| **`calculations`** | Calculator runs, lineage to snapshot — **coordinate with **`snapshots`**. |
| **`snapshots`** | **Frozen contractual JSON** per snapshot version (**`KZO_MVP_SNAPSHOT_V1`** first). |
| **`production`** | Manufacturing orders/routes — **not started** without IDEA. |
| **`supply`** | Procurement / inventory — **not started** without IDEA. |
| **`employee_skills`** | HR/capabilities — **not started** without IDEA. |
| **`analytics`** | Aggregates / KPI sinks — **not started** without IDEA. |

## `product_type` discriminator rule

- Any row that is **not** universal MUST carry **`product_type`** (or equivalent in JSON envelope) allowing future **`CALC_CONFIGURATOR`** vs other modules **without** renaming `public`.

## KZO as consumer

- KZO MVP snapshot inserts belong under **`snapshots`** logically; API path may remain **`/api/kzo/...`** for transport — **URLs are not DB topology**.
