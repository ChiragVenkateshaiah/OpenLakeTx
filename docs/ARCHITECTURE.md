# OpenLakeTx + LakeGuard
## GCP Data Lakehouse Architecture (Industrial Standard)

## 1. Purpose of This Document
This document defines the reference architecture for a production-grade GCP lakehouse platform built using:
- OpenLakeTx - Transaction & consistency layer
- LakeGuard - DataOps, observability, and trust layer

It serves as:
- A single source of truth
- A design guardrail to prevent misalignment

Any future design decisions should be validated against this document

---

## 2. Architectural Philosophy
> Treat data like production software

This platform is designed with separation of concerns:
| Plane                 | Responsibility                   |
| --------------------- | -------------------------------- |
| **Storage Plane**     | Durable, low-cost object storage |
| **Transaction Plane** | ACID, concurrency, versioning    |
| **Operations Plane**  | Data quality, SLAs, trust        |
| **Compute Plane**     | Batch, streaming, analytics      |
| **Consumption Plane** | BI, ML, ad-hoc analysis          |

---

## 3. High-Level Architecture
```pgsql
┌───────────────────────────────────────────────┐
│            BI / Analytics / ML                 │
│     (Dashboards, notebooks, models)            │
└───────────────────────────────────────────────┘
                      ▲
┌───────────────────────────────────────────────┐
│                 Gold Layer                    │
│     Business-ready aggregates & KPIs           │
└───────────────────────────────────────────────┘
                      ▲
┌───────────────────────────────────────────────┐
│                Silver Layer                   │
│   Cleaned, validated, conformed datasets       │
└───────────────────────────────────────────────┘
                      ▲
┌───────────────────────────────────────────────┐
│                Bronze Layer                   │
│   Raw, append-only, immutable ingestion        │
└───────────────────────────────────────────────┘
                      ▲
┌───────────────────────────────────────────────┐
│      OpenLakeTx (Transaction Layer)            │
│  • ACID commits                               │
│  • Optimistic concurrency                     │
│  • Snapshot versioning                        │
│  • Rollback & time travel                     │
└───────────────────────────────────────────────┘
                      ▲
┌───────────────────────────────────────────────┐
│      LakeGuard (DataOps Layer)                 │
│  • Data quality rules                         │
│  • Freshness & SLA enforcement                │
│  • Failure detection                          │
│  • Lineage & audits                           │
└───────────────────────────────────────────────┘
                      ▲
┌───────────────────────────────────────────────┐
│     Google Cloud Storage (GCS)                 │
│   Open formats (Parquet + metadata logs)       │
└───────────────────────────────────────────────┘
```

---

## 4. Technology Stack (GCP)
| Layer          | Technology               |
| -------------- | ------------------------ |
| Object Storage | **Google Cloud Storage** |
| Compute        | **Dataproc** (Spark)     |
| SQL Analytics  | **BigQuery**             |
| Orchestration  | **Cloud Composer**       |
| Monitoring     | **Cloud Monitoring**     |
| Security       | **IAM**                  |


> Important: BigQuery is a consumer, not the storage owner.
> The lakehouse lives on GCS

---

## 5. OpenLakeTx -- Transaction & Control Plane
### Role
OpenLake provides transactional guarantees on object storage, similar to Delta Lake internals.

### Responsibilities
- Atomic multi-file commits
- Optimistic concurrency control
- Versioned snapshots
- Schema validation & evolution
- Failure-safe rollback

### Storage Layout (Example)
```pgsql
/lake/orders/
 ├── data/
 │   ├── part-0001.parquet
 │   └── part-0002.parquet
 └── _openlaketx_log/
     ├── 00000001.json
     └── 00000002.json
```
If a Spark job fails mid-write:
- Partial data is never exposed
- Previous snapshot remains valid
- Recovery is deterministic

---

## 6. LakeGuard -- DataOps & Trust Plane
### Role
LakeGuard ensures data reliability, observability, and trust after each commit.

### Capabilities
| Category     | Examples                           |
| ------------ | ---------------------------------- |
| Data Quality | Nulls, ranges, duplicates          |
| Freshness    | “Silver.orders updated in ≤15 min” |
| Volume       | Sudden spikes or drops             |
| Schema       | Breaking changes                   |
| Lineage      | Bronze → Silver → Gold             |

## Validation Flow
```pgsql
Spark writes data
        ↓
OpenLakeTx commits snapshot
        ↓
LakeGuard validates snapshot
        ↓
❌ Failed → table marked unhealthy
✅ Passed → downstream allowed
```

---

## 7. Orchestration Flow (Production Style)
### Cloud Composer (Airflow) DAG
```markdown
1. Ingest → Bronze
2. OpenLakeTx commit
3. LakeGuard quality checks
4. Transform → Silver
5. OpenLakeTx commit
6. LakeGuard SLA validation
7. Publish → Gold
8. Notify BI / ML consumers
```
Every starge assumes failure is possible.

---

## 8. Security & Governance Model
| Area           | Design                        |
| -------------- | ----------------------------- |
| Storage Access | GCS bucket IAM                |
| Metadata       | Append-only transaction logs  |
| Consumers      | Read-only roles               |
| Audits         | Historical health & snapshots |
| Compliance     | Reproducible data versions    |

---

## 9. Why This is an Industrial-Grade Lakehouse
Typical demo pipelines:
- No transaction safety
- No data trust layer
- No SLA enforcement

This platform:
- Control plane (OpenLakeTx)
- Operations plane (LakeGuard)
- Compute plane (Spark/SQL)
- Storage plane (GCS)

This mirrors real-world data platforms

---

## 10. Intended Audience & Role Alignment
| Role                   | Why This Architecture Fits  |
| ---------------------- | --------------------------- |
| DataOps Engineer       | SLAs, monitoring, failures  |
| Data Platform Engineer | Control plane & governance  |
| Lakehouse Engineer     | ACID on object storage      |
| Cloud Data Engineer    | GCP-native, scalable design |


## 11. Canonical Rule
> If implementation deviates from this document, the implementation is wrong -- not the architecture.

This README is the reference contract for all future work.

---

