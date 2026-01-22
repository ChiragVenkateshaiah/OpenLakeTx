# OpenLakeTx + LakeGuard -- Platform Development Plan (Phase 0)

## 1. Purpose
This document defines the **development plan** for building a production-grade GCP lakehouse platform using OpenLakeTx (transaction & control plane) and LakeGuard (DataOps & trust plane).

It translates the approved references architecture into a phased, execution-ready plan that governs:
- What will be built
- In what order
- With what boundaries
- Under which contracts

This document is binding for implementation.

---

## 2. Canonical References
The following documents are authoritative and must always stay aligned:
- GCP Data Lakehouse Architecture (Industrial Standard) -- architecture reference
- Pull Request Checklist -- governance and change control

If a conflict exists:

> **Architecture -> Development Plan -> Contracts -> Implementation**

---

## 3. Platform Vision

### What This Platform Is
A modular, contract-first lakehouse platform that:
- Provides ACID guarantees on object storage
- Enforces DataOps reliability (quality, freshness, SLAs)
- Separates control, operations, compute, and storage planes
- Mirrors real-world industrial data platforms


### What This Platform Is Not
- Not a demo ETL pipeline
- Not a vendor-locked solution
- Not a UI-heavy BI product
- Not a one-off project

---

## 4. Architectural Alignment
This development plan strictly follows the approved lakehouse architecture:


| Plane                 | Component                        | Responsibility                    |
| --------------------- | -------------------------------- |-----------------------------------|
| **Storage Plane**     | GCS                              | Durabale, low-cost object storage |
| **Transaction Plane** | OpenLakeTx                       | ACID, snapshots, concurrency      |
| **Operations Plane**  | LakeGuard                        | Data quality, SLAs, trust         |
| **Compute Plane**     | Spark (Dataproc)                 | Batch & streaming                 |
| **Consumption Plane** | BigQuery / BI / ML               | Read-only analytics               |

BigQuery is a consumer only. Ownership remains with the lakehouse on GCS

---

## 5. Phase-Based Development Strategy
The platform will be built incrementally using strict phase gates. No phase may begin unless the previous phase is complete and documented

### Phase 0 - Foundation & Contracts
Goal: Design correctness before implementation

Deliverables:

- Platform-development-plan.md (this document)
- Stable folder structure
- Explicit contracts (interfaces only)
- Zero business logic


### Phase 1 - OpenLakeTx Core
Goal: Reliable transactional control plane

Deliverables:

- Snapshot commit engine
- Transaction log writer/reader
- Optimistic concurrency control
- Rollback & recovery semantics


### Phase 2 - LakeGuard Core
Goal: Data trust & observability

Deliverables:

- Data quality rule engine
- Freshness & SLA checks
- Health state registry
- Lineage tracking hooks

### Phase 3 -- Bronze -> Silver -> Gold pipelines
Goal: End-to-End lakehouse workflows

Deliverables:
- Ingestion pipelines
- Transformation patterns
- Contract-enforced promotions


### Phase 4 -- Orchestration & Operations
Goal: Production readiness

Deliverables:
- Airflow DAGs
- Failure handling
- Alerting & notifications

---

## 6. Phase 0 Scope (In Detail)

### 6.1 Folder Structure (Initial)
```text
openlaketx/
├── docs/
│ ├── architecture/
│ ├── development/
│ └── governance/
├── openlaketx/
│ ├── contracts/
│ ├── core/
│ ├── storage/
│ └── utils/
├── lakeguard/
│ ├── contracts/
│ ├── core/
│ └── rules/
└── orchestration/
```
No implementation logic is allowed in Phase 0.


### 6.2 Contract-First Design
All core components must expose contracts before code exists

**OpenLakeTx Contracts (Examples)**
- Transaction lifecycle
- Snapshot visibility rules
- Commit atomicity guarantees
- Schema validation behavior

**LakeGuard Contracts (Examples)**
- Validation input/output schema
- Health state definitions
- Rule execution guarantees
- Failure signaling semantics

Contracts define behavioral expectations, not implementation.

## 7. OpenLakeTx -- Development Principles
- Append-only transaction logs
- Deterministic recovery
- Snapshot immutability
- Compute-agnostic design
- No direct dependency on orchestration

OpenLakeTx must work even without LakeGuard present.

## 8. LakeGuard -- Development Principles
- Read-only access to data
- Triggered only after successful commits
- Non-blocking by default, enforceable by policy
- Auditable and reproducible

LakeGuard must never mutate data

## 9. Failure Is a First-Class Citizen
Every phase assumes:
- Partial writes can occur
- Jobs can fail mid-flight
- Validation can block promotion

Failure handling is designed, not patched.


## 10. Governance Rules
- All changes require PR review
- Architecture alignment is mandatory
- Contracts are versioned
- Breaking changes require explicit documentation

If implementation deviates from architecture:

> The implementation is wrong

## 11. Success Criteria for Phase 0

Phase 0 is complete when:
- This document is finalized
- Folder structure exists
- All contracts exist as empty interfaces
- No implementation logic is present

Only then may Phase 1 begin


## 12. Final Canonical Rule

> Design correctness precedes execution speed

This platform is built to demonstrate engineering maturity, not just working code.
