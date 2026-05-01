# KZO Welded TN Cell DNA

## 1. Purpose

Capture the canonical engineering attribute set for `KZO_WELDED` `TN_CELL` as a separate measurement/voltage-transformer branch object in documentation form.

## 2. Scope: KZO_WELDED / TN_CELL only

This artifact applies only to:

- family: `KZO_WELDED`
- cell type: `TN_CELL`

Out of scope:

- other cell types
- implementation/API/GAS/DB changes

## 3. Cell family classification

`TN_CELL` is a measurement / voltage transformer branch.

Classification rule:

- `TN_CELL` is **not** inherited from `LINE_CELL_FULL_DNA`.

## 4. Attribute list

1. cell number by schematic
2. dispatcher / project line name (same principle as line cell: if project name exists use it; if absent duplicate cell number)
3. bus disconnector type (default: `РВЗ-10/630 ІІІ`)
4. voltage indicators on busbar (`yes` / `no`)
5. surge arrester on busbar (`yes` / `no`)
6. surge arrester on TN side (`yes` / `no`)
7. voltage transformer type (`dry` / `oil`)
8. dry built-in fuses (`yes` / `no`) for dry transformer branch
9. voltage transformer power
10. full voltage transformer name (filtered by previous selections and global manufacturer)

## 5. Dependency rules

- if `voltage_transformer_type = oil`: `dry_built_in_fuses = BLOCKED`
- if `voltage_transformer_type = dry`: `dry_built_in_fuses = REQUIRED`
- `voltage_transformer_full_name` depends on:
  - global voltage transformer manufacturer
  - global rated voltage
  - `voltage_transformer_type`
  - `voltage_transformer_power`
  - `dry_built_in_fuses` where applicable

## 6. Downstream impact map

- dispatcher / project line name -> passport + metal dispatcher marking
- bus disconnector type -> primary circuit, purchasing, BOM
- voltage indicators on busbar -> facade / wiring / BOM
- surge arrester on busbar -> busbar protection / mounting / BOM
- surge arrester on TN side -> transformer protection / mounting / BOM
- voltage transformer type -> compartment layout / mounting / purchasing
- voltage transformer power -> dimensions / mounting / BOM / validation
- voltage transformer full name -> purchasing / passport / BOM

## 7. Passport / dispatcher marking impact

Passport and dispatcher marking are driven by:

- cell number by schematic
- dispatcher / project line name
- voltage transformer full name

Naming rule for dispatcher/project field:

- if project name exists, use project name
- if project name is absent, duplicate cell number

## 8. Purchasing impact

Purchasing-impacting fields in this DNA:

- bus disconnector type
- surge arrester on busbar
- surge arrester on TN side
- voltage transformer type
- voltage transformer power
- voltage transformer full name

## 9. Constructive impact

Constructive/layout-impacting fields in this DNA:

- bus disconnector type
- voltage indicators on busbar
- surge arrester on busbar
- surge arrester on TN side
- voltage transformer type
- voltage transformer power

These fields define TN branch compartment arrangement and mounting requirements.

## 10. Validation notes

- `dry_built_in_fuses` must be blocked for oil transformers.
- `dry_built_in_fuses` must be required for dry transformers.
- `voltage_transformer_full_name` is valid only when dependency inputs are resolved (global manufacturer, global rated voltage, transformer type, power, and dry fuse flag where applicable).
- Dispatcher/project naming must follow the canonical fallback rule: project name first, else cell number.
- Default bus disconnector baseline is `РВЗ-10/630 ІІІ` unless a different selection is explicitly set.

## 11. Unknowns requiring user confirmation

- exact allowed catalog/value list for bus disconnector type beyond default `РВЗ-10/630 ІІІ`
- exact selectable options for voltage indicator and surge arrester families by manufacturer
- final compatibility matrix between transformer power and enclosure volume constraints
- exact project-level rule set for overriding default bus disconnector in atypical TN projects

---

This document is planning/documentation only and contains no implementation changes.
