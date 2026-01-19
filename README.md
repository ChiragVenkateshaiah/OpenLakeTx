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

