# 📘 Control Plane - Metadata Model
**Project: OpenLakeTx + LakeGuard**

**Phase: 1**

**Document Type: Platform Specification**

---

## 1. Purpose of the Metadata Model
The metadata model defines the authoritative state of the lakehouse outside the data itself.

> Data files are not trusted on their own.
>
> Metadata is the source of truth.

This model answers:
- What datasets exist?
- What state are they in?
- Are they promotable?
- Who owns them?
- What happened during execution?



## 2. Design Principles (Non-Negotiable)
1. Metadata is immutable or append-only
2. Metadata is queryable (tables, not logs)
3. Metadata is environment-agnostic
4. Metadata drives behavior (not code flags)
5. Control plane never infers -- it decides


## 3. High-Level Metadata Architecture
```text
LakeGuard Metadata Store (Delta)
 ├── Dataset Registry
 ├── Dataset Versions
 ├── Quality Rules
 ├── Policy Rules
 ├── Promotion Status
 └── Execution Run History
```
All tables are:
- Stored as Delta
- Written only by control plane components
- Readable by OpenLakeTx, tests, and auditors


## 4. Core Metadata Entities (Phase-1)
Phase-1 defines five canonical tables.


## 5. Dataset Registry (`dataset_registry`)
### Purpose
Define what datasets exists in the platform.

> If a dataset is not registered, it does not exist.

### Logical Schema
| Column       | Type      | Description              |
| ------------ | --------- | ------------------------ |
| dataset_id   | string    | Unique identifier        |
| dataset_name | string    | Logical name             |
| domain       | string    | Business/domain grouping |
| layer        | string    | bronze / silver / gold   |
| owner        | string    | Responsible team/person  |
| description  | string    | Human-readable purpose   |
| active       | boolean   | Is dataset enabled       |
| created_at   | timestamp | Registration time        |


### Invariants
- `dataset_id` is immutable.
- A dataset belongs to exactly one layer
- Gold datasets must have a Silver parent


## 6. Dataset Version Registry (`data_versions`)
### Purpose
Tracks every promoted version of a dataset.
> Versions represent approved states, not attempts.

### Logical Schema
| Column       | Type      | Description             |
| ------------ | --------- | ----------------------- |
| dataset_id   | string    | Reference               |
| version      | long      | Monotonic version       |
| snapshot_ref | string    | Table snapshot / commit |
| schema_hash  | string    | Schema fingerprint      |
| row_count    | long      | Rows produced           |
| promoted_at  | timestamp | Promotion time          |
| promoted_by  | string    | Job / pipeline          |

### Invariants
- Versions are append-only
- Version number strictly increase
- No deletion or update allowed

## 7. Execution Run History (`run_history`)
### Purpose
Captures every execution attempt, successful or not.
> This table metadata audit, debugging, and E2E testing.

### Logical Schema
| Column        | Type      | Description                |
| ------------- | --------- | -------------------------- |
| run_id        | string    | Unique run                 |
| dataset_id    | string    | Target dataset             |
| layer         | string    | Execution layer            |
| status        | string    | SUCCESS / FAILED / BLOCKED |
| start_time    | timestamp | Start                      |
| end_time      | timestamp | End                        |
| error_message | string    | Failure reason             |
| triggered_by  | string    | Scheduler / manual         |

### Invariants
- Every run produces exactly one row
- Failures are never overwritten
- Status is terminal


## 8. Quality Rules Registry (`quality_rules`)
### Purpose
Defines what "good data" means.
> Rules are data, not code.

### Logical Schema
| Column          | Type    | Description             |
| --------------- | ------- | ----------------------- |
| rule_id         | string  | Unique rule             |
| dataset_id      | string  | Scope                   |
| layer           | string  | bronze/silver/gold      |
| rule_type       | string  | NOT_NULL, RANGE, UNIQUE |
| rule_expression | string  | Declarative logic       |
| severity        | string  | WARN / FAIL             |
| active          | boolean | Enabled flag            |

### Invariants
- Rules are evaluated before promotion
- FAIL rules block writes
- WARN rules only log


## 9. Policy Registry (`policy_rules`)
### Purpose
Defines platform-level guarantees, not business rules.

Example:
- No PII in Gold
- Schema breaking changes forbidden
- Freshness SLA enforcement

### Logical Schema
| Column            | Type    | Description           |
| ----------------- | ------- | --------------------- |
| policy_id         | string  | Unique policy         |
| applies_to_layer  | string  | silver/gold           |
| policy_type       | string  | SCHEMA / PII / SLA    |
| policy_expression | string  | Declarative condition |
| enforcement       | string  | BLOCK / ALERT         |
| active            | boolean | Enabled               |

### Invariants
- Policies are evaluated before write
- BLOCK policies are absolute
- Policies override pipeline intent


## 10. Promotion Status (`promotion_status`)
### Purpose
Tracks current promotability of datasets.
> This table is how the control plane says "yes" or "no".

### Logical Schema
| Column       | Type      | Description   |
| ------------ | --------- | ------------- |
| dataset_id   | string    | Reference     |
| from_layer   | string    | Source        |
| to_layer     | string    | Target        |
| allowed      | boolean   | Gate result   |
| evaluated_at | timestamp | Decision time |
| reason       | string    | Explanation   |

### Invariants
- Promotion must have a recorded decision
- OpenLakeTx must respect this table
- No silent promotions allowed


## 11. How OpenLakeTx Uses Metadata (Contract)
OpenLakeTx:
- Reads registry, rules, policies
- Writes run history
- Never mutates metadata definitions

LakeGuard:
- Owns all decisions
- Evaluates rules and policies
- Writes promotion outcomes

This separation is strict.


## 12. Failure Model (Designed In)
| Scenario         | Metadata Outcome           |
| ---------------- | -------------------------- |
| Job crash        | run_history = FAILED       |
| Rule violation   | promotion_status = BLOCKED |
| Policy violation | promotion_status = BLOCKED |
| Partial write    | No version recorded        |

Metadata always reflects truth, not intent.


## 13. Why this Metadata Model Matters
This enables:
- End-to-End Testing
- Deterministic replay
- Trust scoring
- Audit readiness
- Platform observability

Most projects skip this.
That's why most platforms fail later.


## 14. Phase-1 Exit Criteria (Metadata)
Phase-1 metadata is complete when:
- All tables are defined
- Invariants are documented
- OpenLakeTx <-> LakeGuard responsibilities are clear
- Promotion decisions are metadata-driven

## Summary
> Data moves because metadata allows it -- Not because code ran.