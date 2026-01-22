# 📘 Control Plane -- Quality Rules & Enforcement Model

**Project: OpenLakeTx + LakeGuard**
**Phase: 1**
**Document Type: Platform Specification**

---

## 1. Purpose of Quality Rules
Quality rules define whether data is fit to move forward in the lakehouse
> Pipeline may run, but data only progresses if quality allows it.

This model answers:
- What does "good data" mean?
- When is data blocked?
- Who decides pass/fail?
- How is failure recorded?


## 2. Design Principles (Non-Negotiable)
1. Quality is declarative, not embedded in code
2. Rules are evaluated before promotion
3. Failures block progression by default
4. Results are persisted as metadata
5. Quality applies progressively by layer


## 3. Quality in the Lakehouse Context
| Layer  | Quality Intent         |
| ------ | ---------------------- |
| Bronze | Structural correctness |
| Silver | Business correctness   |
| Gold   | Analytical correctness |

Each layer tightens constraints.


## 4. Ownership & Responsibility
| Component      | Responsibility                |
| -------------- | ----------------------------- |
| OpenLakeTx     | Executes data transformations |
| LakeGuard      | Evaluates quality rules       |
| Metadata Store | Persists rules & outcomes     |

❗ OpenLake never decides data quality outcomes.

## 5. Quality Rule Lifecycle
Rule lifecycle states
```
DEFINED -> ACTIVE -> (PASS | FAIL) -> RECORDED
```
- Rules are defined once
- Activated explicitly
- Evaluated on every eligible run
- Results are immutable

## 6. Quality Rule Types (Phase-1)
Phase-1 supports foundational rule categories.

### 6.1 Structural Rules
Applied primarily in Bronze.

Examples:
- Schema match
- Column existence
- Data type validation

Failure impact:
- Promotion blocked

### 6.2 Completeness Rules
Applied in Bronze & Silver.

Examples:
- NOT NULL checks
- Mandatory field presence

Failure impact:
- WARN or FAIL (rule-driven)

### 6.3 Validity Rules
Applied mainly in Silver.

Examples:
- Range checks
- Enum validation
- Referential consistency

Failure impact:
- Promotion blocked

### 6.4 Uniqueness Rules
Applied in Silver.

Examples:
- Primary key uniqueness
- Deduplication thresholds

Failure impact:
- Promotion blocked

### 6.5 Aggregate Integrity Rules
Applied in Gold.

Examples:
- Count reconciliation
- Metric sanity checks

Failure impact:
- ❌ Gold publication blocked


## 7. Rule Definition Model (Metadata-Driven)
Rules are stored in the `quality_rules` metadata table (already defined)

### Conceptual rule example
```vbnet
rule_type: NOT_NULL
rule_expression: order_id IS NOT NULL
severity: FAIL
layer: silver
```
Key characteristics:
- Expressions are declarative
- Engine-agnostic
- Interpreted by LakeGuard


## 8. Enforcement Semantics
### Severity Levels
| Severity | Behavior        |
| -------- | --------------- |
| WARN     | Log only        |
| FAIL     | Block promotion |

Default behavior:
> FAIL unless explicitly downgraded

## 9. Enforcement Timing (Critical)
Quality rules are evaluated at strict enforcement points.
| Stage               | Enforcement          |
| ------------------- | -------------------- |
| Before Silver write | Bronze quality rules |
| Before Gold write   | Silver + Gold rules  |
| After write         | Metrics & audit only |

> ❗ No retroactive quality decisions.

## 10. Quality Evaluation Flow
```
OpenLakeTx completes transformation
        ↓
LakeGuard fetches applicable rules
        ↓
Rules evaluated on dataset
        ↓
Results persisted
        ↓
Promotion allowed or blocked
```

## 11. Quality Result Recording
Every evaluation produces immutable results.

### Conceptual result fields
| Field         | Description         |
| ------------- | ------------------- |
| run_id        | Execution reference |
| rule_id       | Quality rule        |
| result        | PASS / FAIL         |
| evaluated_at  | Timestamp           |
| failure_count | Optional metric     |

These results are never overwritten.

## 12. Failure Behavior (Designed, Not Accidental)
| Scenario            | Outcome           |
| ------------------- | ----------------- |
| Single FAIL rule    | Promotion blocked |
| Multiple FAIL rules | Promotion blocked |
| WARN-only failures  | Promotion allowed |
| Evaluation error    | Promotion blocked |

> Quality uncertainty defaults to safety

## 13. Interaction with Promotion Gates
Quality is a hard dependency for promotion
| Transition      | Required                     |
| --------------- | ---------------------------- |
| Bronze → Silver | All Bronze rules PASS        |
| Silver → Gold   | All Silver + Gold rules PASS |

Promotion gates cannot override quality.


## 14. What Quality Rules Do Not Do
Explicitly excluded:
- Data correction
- Auto-fixing values
- Backfilling data
- SLA evaluation
- PII detection (Policy layer)

These belong to other control-plane components

## 15. Why This Model Matters
This model ensures:
- Deterministic behavior
- Testable guarantees
- Auditable outcomes
- Zero silent data corruption

Most pipelines fail silently
This platform cannot.

## 16. Phase-1 Exit Criteria (Quality)
Quality model is complete when:
- Rule types are defined
- Enforcement points are explicit
- Failure bahavior is deterministic
- Metadata recording is mandatory

## Final Control Plane Guarantee (Quality)
> No dataset advances unless it proves it deserves to.

This is industrial-grade lakehouse quality enforcement.

