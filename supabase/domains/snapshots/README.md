# Domain: snapshots — calculation snapshot persistence

## Scope

Stores **immutable (append / insert-only)** frozen calculation objects. **System table:** **`public.calculation_snapshots`** (Stage **8A.0.1**). **KZO** is the first consumer: **`product_type = 'KZO'`** on each row; **`snapshot_version`** = **`KZO_MVP_SNAPSHOT_V1`** (contract id from Stage **7B**).

## Rules

1. **Truth upstream**: snapshot JSON matches **`prepare_calculation`** + layer contract only after **Freeze** (**Stage 7B**).
2. **Persistence does not reshape**: **`POST /api/kzo/save_snapshot`** validates + inserts; **no** ERP unpacking of JSON blobs in Stage **8A.x** MVP.
3. **Registry linkage**: **`calculation_snapshots`** in **`schema_registry/REGISTRY_INDEX.md`**.
4. **Naming**: Root table MUST stay product-neutral (**`calculation_snapshots`**). **Never** reintroduce **`kzo_*`** as the shared snapshot hub for EDS Power. Expanding **`product_type`** beyond **`KZO`** requires CHECK migration + IDEA.
