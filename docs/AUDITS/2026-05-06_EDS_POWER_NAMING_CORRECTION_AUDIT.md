# 2026-05-06 — EDS Power Naming Correction Audit

## Objective

Apply governance naming correction so current project documentation uses EDS Power terminology and reserves Sakura/SakuraCore naming for a future separate project.

## Reason for correction

Sakura/SakuraCore terms started appearing in active EDS Power architecture governance docs and could become deeply embedded.

Correction intent:
- current system canonical naming: EDS Power / EDS Power Client Core / EDSPowerCore
- Sakura/SakuraCore reserved for future separate project naming only

## Rename map applied

- Sakura Terminal Fleet Governance -> EDS Power Terminal Fleet Governance
- Sakura Minimal Local Bootstrap Contract -> EDS Power Minimal Local Bootstrap Contract
- Sakura Central GAS Core Contract -> EDS Power Client Core Contract
- Sakura Dynamic Menu Payload Contract -> EDS Power Dynamic Menu Payload Contract
- Sakura Terminal Assignment Doctrine -> EDS Power Terminal Assignment Doctrine
- Sakura Admin Provisioning Doctrine -> EDS Power Admin Provisioning Doctrine
- SakuraCore -> EDSPowerCore (documentation terminology only)
- SAKURA_* idea handles -> EDS_POWER_* idea handles

## Files renamed

- `docs/ARCHITECTURE/SAKURA_TERMINAL_FLEET_GOVERNANCE.md` -> `docs/ARCHITECTURE/EDS_POWER_TERMINAL_FLEET_GOVERNANCE.md`
- `docs/ARCHITECTURE/SAKURA_MINIMAL_LOCAL_BOOTSTRAP_CONTRACT.md` -> `docs/ARCHITECTURE/EDS_POWER_MINIMAL_LOCAL_BOOTSTRAP_CONTRACT.md`
- `docs/ARCHITECTURE/SAKURA_CENTRAL_GAS_CORE_CONTRACT.md` -> `docs/ARCHITECTURE/EDS_POWER_CLIENT_CORE_CONTRACT.md`
- `docs/ARCHITECTURE/SAKURA_DYNAMIC_MENU_PAYLOAD_CONTRACT.md` -> `docs/ARCHITECTURE/EDS_POWER_DYNAMIC_MENU_PAYLOAD_CONTRACT.md`
- `docs/ARCHITECTURE/SAKURA_TERMINAL_ASSIGNMENT_DOCTRINE.md` -> `docs/ARCHITECTURE/EDS_POWER_TERMINAL_ASSIGNMENT_DOCTRINE.md`
- `docs/ARCHITECTURE/SAKURA_ADMIN_PROVISIONING_DOCTRINE.md` -> `docs/ARCHITECTURE/EDS_POWER_ADMIN_PROVISIONING_DOCTRINE.md`
- `docs/AUDITS/2026-05-06_SAKURA_TERMINAL_FOUNDATION_SKELETON.md` -> `docs/AUDITS/2026-05-06_EDS_POWER_TERMINAL_FOUNDATION_SKELETON.md`

## References updated

Updated references and governance records in:
- `docs/NOW.md`
- `docs/CHANGELOG.md`
- `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`
- `docs/AUDITS/00_AUDIT_INDEX.md`
- `docs/ARCHITECTURE/EDS_POWER_TERMINAL_FLEET_GOVERNANCE.md`
- `docs/ARCHITECTURE/EDS_POWER_CLIENT_CORE_CONTRACT.md`
- `docs/ARCHITECTURE/EDS_POWER_MINIMAL_LOCAL_BOOTSTRAP_CONTRACT.md`

## Remaining code-level Sakura references

The following are intentionally left unchanged in this governance patch and require a separate implementation-safe rename task:
- `gas/core/SakuraCore.gs` (function names/constants/menu labels)
- `gas/terminal/SakuraLocalBootstrap.gs` (function names/constants/messages)

Reason:
- current task scope is documentation + naming governance only
- code rename can break skeleton wiring and needs separate bounded implementation task

## Remaining documentation Sakura references

Some older Module 01 historical audit records still contain Sakura wording as historical context (for example, previously recorded Sakura login wording in legacy audit entries).

These are retained in this patch to avoid rewriting historical factual records beyond active architecture/governance naming correction scope.

## What was NOT changed

- No GAS logic changes
- No API changes
- No DB schema changes
- No SQL
- No Render/env changes
- No module/business/engineering implementation

## Verdict

EDS Power naming governance correction applied successfully for active architecture/governance docs.
Architecture logic unchanged. No implementation drift.
