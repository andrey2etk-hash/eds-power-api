# Gemini Focused Audit Request — Stage 8B.2D

Scope: **one bounded focused audit cycle only** under Governance Audit Budget Control (`docs/00_SYSTEM/02_GLOBAL_RULES.md` §19).

## Primary File Under Review

- `docs/AUDITS/2026-05-01_STAGE_8B_2D_INTEGRITY_STANCE_V1_ENFORCEMENT_DOCTRINE.md`

## Read-Only Context

- `docs/AUDITS/2026-04-30_STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE.md`
- `docs/AUDITS/2026-04-30_STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE.md`
- `docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE.md`
- `docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`
- `docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`
- `docs/AUDITS/2026-04-30_STAGE_8B_2D_INTEGRITY_STANCE_V1_ENFORCEMENT_IDEA_NORMALIZATION.md`

## Audit Role

External critical governance auditor.

Validate:
- boundedness of `2D`,
- V1 protection without redesign,
- structural integrity doctrine correctness,
- five-layer enforcement clarity,
- `logic_version` governance,
- incomplete vs corrupted distinction,
- `L3` vs `L4` boundary integrity,
- API final authority,
- client thinness,
- no scope bleed into `2A` / `2B` / `2C` / `2E`.

## Strict Forbidden in Findings

Do not require:
- code changes,
- API redesign,
- GAS changes,
- DB changes,
- V1 field additions,
- `2E` doctrine opening,
- implementation tasks.

If such work appears necessary, mark **DEFERRED** only.

## Mandatory Checks

1. Full structure completeness of the `2D` dossier.
2. Definitions quality: valid / incomplete / corrupted snapshot.
3. Five-layer mandatory governance clarity.
4. `logic_version` correlation governance clarity.
5. `L3`/`L4` enforcement split correctness.
6. API final authority clarity.
7. Client cannot self-certify validity.
8. No V1 redesign/mutation pressure.
9. No implementation leakage.
10. Next step bounded to focused closeout only.

## Output Format (Required)

- `PASS CLEAN`
- `PASS WITH DOC FIXES`
- `BLOCKED`

If `PASS WITH DOC FIXES` or `BLOCKED`:
- provide exact doc-only wording changes (file + section + replacement text).

## Closeout Path

- `docs/AUDITS/YYYY-MM-DD_GEMINI_STAGE_8B_2D_FOCUSED_AUDIT.md`

## Final Rule

- No master audit.
- No post-fix loop unless verdict is `BLOCKED`.
