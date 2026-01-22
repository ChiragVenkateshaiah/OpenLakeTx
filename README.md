# Open Lakehouse Platform (OpenLakeTx + LakeGuard)

## Platform-First GCP Data Lakehouse
This repository contains a production-grade, platform-first data lakehouse design built on Google Cloud Platform(GCP)

The platform is designed around clear separation of concerns:
- OpenLakeTx - transactional safety & control plane
- LakeGuard - DataOps, observability, and trust plane

This is not a collection of ad-hoc pipelines, but a governed data platform intended to scale across teams and domains.

---

## Repository Structure
The repository is organized to reflect real data platform ownership boundaries rather than individual pipelines

```sql
.
├── .github/
│   └── pull_request_template.md
│
├── docs/
│   ├── architecture.md
│   ├── design-decisions.md
│   └── pr-checklist.md
│
├── openlaketx/
│   ├── core/
│   ├── commit/
│   ├── metadata/
│   └── recovery/
│
├── lakeguard/
│   ├── quality/
│   ├── sla/
│   ├── lineage/
│   └── alerts/
│
├── pipelines/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── infra/
│   ├── gcp/
│   └── orchestration/
│
├── CONTRIBUTING.md
└── README.md
```

---

## Folder Breakdown

### `.github/`
GitHub-native configuration used to enforce platform discipline.

- `pull_request_template.md`
Enforced PR checklist that ensures:
- Architectural alignment
- Transactional safety
- DataOps SLAs
- Observability & governance

> This is where discipline is enforced, not documented.


### `doc/`
Canonical documentation for the platform.
These files are treated as contracts, not optional docs.

- `architecture.md`
Defines the reference GCP lakehouse architecture

- `design-decisions.md`
Records explicit tradeoffs and rationale

- `pr-checklist.md`
Platform governance and change-control rules
> If implementation conflicts with these documents, the implementation is wrong.


### `openlaketx/` -- Transaction & control plane of the lakehouse
This directory contains the **transactional core** of the lakehouse

It is responsible for **ACID guarantees on object storage**, independent of compute engines.

Submodules:
- `core/` - core abstractions and state handling
- `commit/` - atomic commit protocol and concurrency control
- `metadata/` - table metadata, snapshots, schema state
- `recovery/` - rollback, retries, and failure handling

Responsible for:
- ACID commit semantics on object storage
- Optimistic concurrency control
- Snapshot versioning & rollback
- Schema and metadata coordination

**Important rule:**
No Spark, pipeline, or business logic is allowed in this layer.

This layer is **engine-agnostic** and intentionally isolated from compute logic


### `lakeguard/` -- DataOps & trust plane of the platform.
This directory contains the **operational brain** of the platform

LakeGuard ensures that only trusted data progresses downstream.

Submodules:

- `quality/` - data quality rules and validations
- `sla/` - freshness and latency enforcement
- `lineage/` - Bronze -> Silver -> Gold tracking
- `alerts/` - failure notifications and health signals

Responsible for:
- Data quality validation
- Freshness & SLA enforcement
- Failure classification
- Lineage and health tracking

LakeGuard treats data quality as a gate, not a report.


### `pipelines/` -- Compute Only (No Guarantees)

Compute logic only -- no platform guarantees live here.

- `bronze/` - raw, append-only ingestion
- `sivler/` - cleaned and validated datasets
- `gold/` - business-level aggregates

#### pipeline assume:
- Transactions are already safe (OpenLakeTx)
- Data trust is externally enforced (LakeGuard)


### `infra/` -- Infrastructure and orchestration definitions.

- `gcp/`
GCS, IAM, Dataproc, BigQuery integration.

- `orchestration/`
Airflow / Cloud Composer DAGs

This separation prevents **infra logic from leaking into data logic**


### `CONTRIBUTING.md`
Defines how changes are made, reviewed, and merged.

#### Key principles:
- Platform guarantees > feature speed
- All PRs must complete the PR checklist
- Architectural drift is explicitly rejected

---

## Architecture & Governance
This project follows a platform-first lakehouse architecture.

Reference documents:
- [Architecture Overview](/docs/ARCHITECTURE.md)
- [Design Decisions & Tradeoffs](/docs/design-decisions.md)
- [Pull Request Checklist](/docs/pr-checklist.md)
- [Platform Development Plan](/docs/platform-development-plan.md)


All changes are governed through an enforced PR checklist to prevent architecutural drift and silent degradation


---

## Design Philosophy
- Data is treated as production software
- Failures are expected and designed for
- Guarantees are enforced at the platform layer
- Pipelines are replaceable, platforms are not


---

## Intended Audience
This repository is designed for:
- Data Platform Engineers
- DataOps Engineers
- Lakehouse Engineers
- Cloud Data Engineers (GCP)

---

## Canonical Rule

> Architecutre lives in docs

> Discipline lives in PRs

> Trust lives in enforcement

