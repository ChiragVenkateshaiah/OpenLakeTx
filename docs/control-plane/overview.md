# Phase-1: Control Plane Documentation

#### Project: OpenLakeTx + LakeGuard
#### Phase: 1 - Control Plane Foundation
#### Audience: Platform Engineers, Data Engineers, Reviewers

This Control Plane is designed before any data-plane code to ensure
governance, quality, and promotion semantics are explicit, testable,
and non-bypassable.


## 1. Purpose of the Control Plane
The Control Plane governs how data is allowed to move through the lakehouse.

> OpenLakeTx executes data.

> LakeGuard control data.

The Control Plane ensures:
- Data quality is enforced
- Policies are applied consistently
- Bad data is blocked early
- Every dataset is auditable and trusted


## 2. Control Plane vs Data Plane (clear separation)

| Plane         | Responsibility            | Owned By   |
| ------------- | ------------------------- | ---------- |
| Data Plane    | Ingest, transform, store  | OpenLakeTx |
| Control Plane | Govern, validate, observe | LakeGuard  |

This separation is intentional and architectural.


## 3. Control Plane Scope (Phase-1)

Included in Phase-1
- Metadata registry
- Data quality rules
- Policy enforcement points
- Promotion gates
- Audit & run tracking
- Control <-> execution interfaces


Explicity excluded (future phases)
- UI / Dashboards
- Advanced ML-based anomaly detection
- Multi-tenant access control


## 4. Core Control Plane Responsibilities

### 4.1 Metadata Management
The Control Plane maintains **authoritative metadata** about datasets.


Each dataset must have:
- Name & domain
- Layer (Bronze/Silver/Gold)
- Schema definition
- Owner
- Quality expectations
- Promotion eligibility

Metadata is stored as Delta tables and treated as data itself.


### 4.2 Data Quality Enforcement
Quality rules are:
- Explicit
- Declarative
- Layer-specific

Examples:
- Bronze: Schema + basic null checks
- Silver: business rules, deduplication
- Gold: aggregation integrity

> No dataset moves forward unless quality passes


### 4.3 Policy Enforcement
Policies define platform guarantees, not business logic.


Examples:
- Schema drift allowed? (Bronze only)
- PII columns allowed? (never in Gold)
- Freshness SLA met?

> Policies are evaluated before write operations



### 4.4 Promotion Gates (Critical Concept)

Promotion between layers is conditional:
| Transition      | Gate                   |
| --------------- | ---------------------- |
| Bronze → Silver | Schema + quality pass  |
| Silver → Gold   | Quality + policy + SLA |


If a gate fails:
- Write is blocked
- Job is marked failed
- Audit record is written

### 4.5 Audit & Observability
Every execution produces:
- Run ID
- Start / end time
- Status
- Row counts
- Rule evaluation results

This enables:
- Debugging
- Trust scoring
- E2E testing validation



## 5. Control Plane Architecture

### Key components
```pgsql
LakeGuard
 ├── Metadata Registry
 ├── Rule Engine
 ├── Policy Engine
 ├── Promotion Gatekeeper
 └── Audit Store
```

> LakeGuard never transform data -- it only decides whether it is allowed to proceed.


## 6. OpenLakeTx <-> LakeGuard Interface (Contract)
This interface is the **heart of Phase-1**

#### Control Hooks
OpenLakeTx must call LakeGuard at:
1. Before writing Silver
2. Before writing Gold
3. After each successful write

#### Example interaction (conceptual)
```text
OpenLakeTx → LakeGuard:
"Can I promote dataset X to Silver?"

LakeGuard:
- Evaluate rules
- Evaluate policies
- Return ALLOW / BLOCK

No bypass is allowed
```

## 7. Failure Behavior (Defined, Not Accidental)
If control checks fail:
- Data is NOT written
- Downstream layers do NOT run
- Failure is good
- Metadata updated

This is intentional fail-fast behavior.


## 8. Folder Structure (Phase-1)

Recommended structure:
```markdown
docs/
 └── control-plane/
      ├── overview.md
      ├── responsibilities.md
      ├── metadata-model.md
      ├── quality-rules.md
      ├── policy-enforcement.md
      ├── promotion-gates.md
      └── interfaces.md
```

This mirrors real platform documentation, not notebooks.


## 9. Non-Goals (Important for reviewers)
Phase-1 does not aim to:
- Compete with Unity Catalog
- Build a UI
- Handle all edge cases

It aims to:
> Prove correct platform design and control thinking


## 10. Phase-1 Exit Criteria (very important)
Phase-1 is complete when:
- Control responsibilities are documented
- Metadata model is defined
- Enforcement points are explicit
- OpenLakeTx <-> LakeGuard contract is clear.


## 11. Control Plane Documentation Map

This document provides the high-level intent and scope of the Control Plane.
Detailed specifications are defined in the following documents:

1. **Metadata Model**
   - Defines the authoritative metadata tables used by the Control Plane
   - Dataset registry, versions, run history, quality rules, policy rules
   - See: [metadata-model.md](/docs/control-plane/metadata-model.md)

2. **Quality Rules & Enforcement**
   - Defines how data quality is declared, evaluated, and enforced
   - Layer-specific quality semantics (Bronze / Silver / Gold)
   - See: [quality-rules.md](quality-rules.md)

3. **Policy Enforcement Model**
   - Defines non-negotiable platform policies
   - Schema evolution, PII constraints, freshness SLAs
   - See: [policy-enforcement.md](policy-enforcement.md)

4. **Promotion Gates & State Transitions**
   - Defines how datasets move between layers
   - Promotion states, gate evaluation order, failure behavior
   - See: [promotion-gates.md](promotion-gates-states.md)

Only after this do we write any production code.