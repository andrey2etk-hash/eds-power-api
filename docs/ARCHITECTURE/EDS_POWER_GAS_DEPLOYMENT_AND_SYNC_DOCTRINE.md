# EDS Power GAS Deployment and Sync Doctrine

## 1. Purpose

Define how GAS files are **organized**, **deployed**, and **synchronized** into bound Google Sheet terminals so repo truth and bound Apps Script projects stay aligned as the terminal UI shell grows.

## 2. Problem

Manual copying of GAS files can create **drift** between the repository and bound Apps Script projects.

**Observed during DB-driven menu validation:**

- Bound script initially contained only `EDSPowerCore.gs` and `EDSPowerLocalBootstrap.gs`.
- Auth-related files were **missing** from the bound project.
- **Manual sync** was required to add, at minimum:
  - `AuthSession.gs`
  - `AuthTransport.gs`
  - `AuthMenu.gs`
  - `AuthLoginDialog.html`

Without a recorded sync discipline, operators cannot know which commit/version a Sheet terminal actually runs.

## 3. Current Manual Sync Model

Until an **automated** deployment pipeline exists:

- The **repository** is the **source of truth**.
- The **operator** manually copies **approved** GAS file contents into the bound Apps Script project.
- **Every** manual sync must be **recorded** (commit hash or tag, date, scope of files synced, operator test outcome where applicable).
- **No** untracked manual code edits in Apps Script — or they must be explicitly labeled **temporary diagnostic** and either reverted or backported to repo under a TASK.

## 4. Required GAS File Groups

### Group A — Local Bootstrap

- `gas/terminal/EDSPowerLocalBootstrap.gs`

**Purpose:**

- `onOpen`  
- terminal context  
- bootstrap bridge  
- stable local entry points  

### Group B — Core

- `gas/core/EDSPowerCore.gs`

**Purpose:**

- render menu  
- call backend menu endpoint  
- open sidebar/modal **entry points** in future (thin wiring — no business logic)  
- thin client transport/render only  

### Group C — Auth

- `gas/AuthSession.gs`  
- `gas/AuthTransport.gs`  
- `gas/AuthMenu.gs`  
- `gas/AuthLoginDialog.html`  

**Purpose:**

- login dialog  
- session storage  
- bearer token helper  
- session status  
- logout  

### Group D — Optional Demo / Test

- `gas/Module01DemoClient.gs`  
- `gas/Stage3D_KZO_Handshake.gs`  

**Purpose:**

- demo only  
- **not** required for production terminal shell unless explicitly approved  

## 5. Sync Rules

Before operator testing, the bound Apps Script project must contain **all** files **required** for the feature under test (per groups above and any task-specific addendum).

**Manual sync steps:**

1. Confirm **repo commit/version** to sync from.  
2. Copy **full** file contents from repo into matching Apps Script file names.  
3. Preserve **HTML** file names **exactly** (e.g. dialog HTML).  
4. Save the Apps Script project.  
5. Reload the Google Sheet.  
6. Run the operator test.  
7. Record **sync evidence** (audit note, checklist, or changelog entry as governance requires).  

## 6. No Silent GAS Drift

Operators and agents must **not** edit GAS directly in Apps Script without later:

- reflecting the change in the **repository**, or  
- explicitly marking the change as **temporary diagnostic** with an owner and expiry/gate to remove or merge.

Silent drift invalidates terminal verification claims against repo state.

## 7. Future Deployment Options

**Possible** future automation (no implementation authorized by this document):

- clasp-based deployment  
- Apps Script API deployment  
- terminal template cloning workflow  
- versioned EDSPowerCore library  

Selection and implementation are **separate** governance tasks.

## 8. Required Future Decision

Before **multiplying** terminal copies across a fleet:

**Choose a canonical deployment method for GAS** (manual sync + recorded evidence vs clasp vs library vs other) and record it in architecture/closeout docs.

## 9. Verdict

**`GAS_DEPLOYMENT_AND_SYNC_DOCTRINE_READY_FOR_AUDIT`**
