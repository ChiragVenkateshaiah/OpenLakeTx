# 📘 Control Plane -- Promotion Gates & State Transitions

Project: OpenLakeTx + LakeGuard

Phase: 1

Document Type: Platform Specification

## 1. Purpose of Promotion Gates
Promotion gates define when data is allowed to move forward in the lakehouse.

> Pipelines may execute freely.
>
> Promotion is earned, not assumed.

Promotion gates:
- Enforce quality and policy outcomes
- Protecct downstream layers
- Make platform behavior predictable
- Enable deterministic E2E testing

## 2. Promotion as a Controlled State Machine
Promotion is modeled as a finite state machine.

### Dataset Promotion States
| State      | Meaning                         |
| ---------- | ------------------------------- |
| REGISTERED | Dataset defined, never promoted |
| ELIGIBLE   | Candidate for promotion         |
| BLOCKED    | Promotion denied                |
| PROMOTED   | Version published               |

States are layer-scoped, not global.

## 3. Promotion Scope
Promotion applies only to:
- Bronze -> Silver
- Silver -> Gold

There is:
- ❌ No skipping layers
- ❌ No direct Gold ingestion
- ❌ No forced promotion


## 4. Gate Evaluation Inputs
Promotion gates evaluate only control-plane signals.

| Input            | Source           |
| ---------------- | ---------------- |
| Dataset registry | Metadata         |
| Policy results   | LakeGuard        |
| Quality results  | LakeGuard        |
| Execution status | Run history      |
| Previous version | Dataset versions |

No pipeline logic participates

## 5. Gate Evaluation Order (Strict)
Evaluation order is fixed and intentional.
```markdown
1. Dataset eligibility
2. Execution success
3. Policy enforcement
4. Quality enforcement
5. Promotion decision
```
Failure at any step stops evaluation.


## 6. Bronze -> Silver Promotion Gate
Preconditions
- Dataset registered in Bronze
- Successful Bronze execution
- All Bronze-level policies = ALLOW
- All Bronze quality rules = PASS

Outcomes
| Condition         | Result   |
| ----------------- | -------- |
| All checks pass   | PROMOTED |
| Any policy fails  | BLOCKED  |
| Any quality fails | BLOCKED  |
| Execution failed  | BLOCKED  |

## 7. Silver -> Gold Promotion Gate
Preconditions
- Dataset registered in Silver
- Successful Silver execution
- All Silver + Gold policies = ALLOW
- All Silver + Gold quality rules = PASS
- SLA / Freshness checks satisfied

Outcomes
| Condition         | Result           |
| ----------------- | ---------------- |
| All checks pass   | PROMOTED         |
| Any policy fails  | BLOCKED          |
| Any quality fails | BLOCKED          |
| SLA violated      | BLOCKED or ALERT |


## 8. State Transition Rules
Valid Transitions
```markdown
REGISTERED → ELIGIBLE
ELIGIBLE → PROMOTED
ELIGIBLE → BLOCKED
BLOCKED → ELIGIBLE (after remediation)
```

Invalid Transitions (Forbidden)
```markdown
PROMOTED → BLOCKED
PROMOTED → ELIGIBLE
BLOCKED → PROMOTED (without reevaluation)
```
Promotion is monotonic per version.

## 9. Versioning Semantics
Each promotion produces:
- A new immutable dataset version
- A snapshot reference
- A recorded promotion event

❗ Failed promotions do not create versions.


## 10. Recording Promotion Decisions
Promotion outcomes are persisted in `promotion_status`

#### Conceptual fields
| Field        | Description                |
| ------------ | -------------------------- |
| dataset_id   | Dataset                    |
| from_layer   | Source layer               |
| to_layer     | Target layer               |
| decision     | PROMOTED / BLOCKED         |
| evaluated_at | Timestamp                  |
| reason       | Human-readable explanation |

This table is authoritative

## 11. Failure Behavior (Designed-In)
| Failure Scenario         | Result  |
| ------------------------ | ------- |
| Partial data write       | BLOCKED |
| Quality evaluation error | BLOCKED |
| Policy evaluation error  | BLOCKED |
| Metadata unavailable     | BLOCKED |

> Promotion never proceeds under uncertainity.

## 12. Interaction with OpenLakeTx
OpenLakeTx:
- Requests promotion eligibility
- Executes data processing
- Respects promotion decisions
- Never forces writes

LakeGuard:
- Owns evaluation
- Writes promotion outcomes
- Blocks or allows progression

This contract is **non-negotiable**


## 13. Deterministic E2E Testing Enablement
Because promotion is metadata-driven, tests can assert:
- Promotion allowed when expected
- Promotion blocked on rule violation
- No version created on failure
- Correct reason recorded

This makes end-to-end testing first-class

## 14. What Promotion Gates Do NOT Do
Explicit exclusions:
- Data correction
- Retry logic
- Backfills
- Overrides
- Human approval workflows

These belong to future phases.

## 15. Phase-1 Exit Criteria (Promotion)
Phase-1 is complete when:
- Promotion states are defined
- Transitions are deterministic
- Enforcement order is fixed
- Decisions are persisted
- OpenLakeTx contract is clear


## ✅ Canonical Promotion Guarantee
> Data advances only when the platform explicitly allows it.

This is the core trust mechanism of your lakehouse.
