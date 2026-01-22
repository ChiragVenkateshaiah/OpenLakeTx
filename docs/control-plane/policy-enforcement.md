# 📘 Control Plane - Policy Enforcement Model
Project: OpenLakeTx + LakeGuard

Phase: 1

Document Type: Platform Specification

## 1. Purpose of Policy Enforcement
Policies define non-negotiable platform guarantees

> Quality asks: *"Is the data correct?"*
>
>Policy asks: *"Is this data allowed to exist here at all?"*

Policy enforcement ensures:
- Platform rules override pipeline intent
- Governance is consistent
- Violations are blocked deterministically
- No silent exceptions exist

## 2. Policy vs Quality (Critical Distinction)
| Dimension        | Quality Rules    | Policy Rules            |
| ---------------- | ---------------- | ----------------------- |
| Scope            | Dataset-specific | Platform-wide           |
| Intent           | Data correctness | Governance & compliance |
| Flexibility      | WARN or FAIL     | Always enforced         |
| Override allowed | No               | No                      |
| Owner            | Data domain      | Platform                |


> Quality validates data. Policy constrains behavior

## 3. Design Principles (Non-Negotiable)
1. Policies are absolute
2. Policies are evaluated before data is written
3. Policies cannot be bypassed
4. Policy violations block execution
5. Policy decisions are recorded as metadata

## 4. Policy Categories (Phase-1 Scope)
Phase-1 supports foundational policy types that every enterprise lakehouse requires

### 4.1 Schema Evolution Policy
Controls how schemas may change across versions.

Allowed:
- Additive columns
- Nullable relaxations

Blocked:
- Column removal
- Type narrowing
- Semantic breaking changes

Evaluated:
- Before Silver and Gold writes


### 4.2 PII / Sensitive Data Policy
Controls where sensitive data may exist.

Rules:
- PII allowed in Bronze (raw)
- Restricted in Silver
- Forbidden in Gold

Evaluation:
- Column metadata
- Schema annotations
- Explicit deny-list

Violation -> Hard block 

### 4.3 Data Freshness / SLA Policy
Ensures datasets meet timeliness guarantees.

Rules:
- Maximum staleness per layer
- Expected update frequency

Evaluation:
- Compare current run time vs last successful promotion

Violation:
- BLOCK or ALERT (policy-driven)


### 4.4 Layer Boundary Policy
Ensures semantic purity of layers.

Examples:
- Bronze cannot aggregate
- Gold cannot contain raw identifiers
- Silver must be deduplicated

Prevents architectural drift.


## 5. Policy Definition Model (Metadata-Driven)
Policies are stored in the `policy_rules` table.

Conceptual policy example
```makefile
policy_type: SCHEMA_EVOLUTION
applies_to_layer: gold
policy_expression: no_breaking_changes
enforcement: BLOCK
```
Key characteristics:
- Declarative
- Environment-agnostic
- Evaluated by LakeGuard

## 6. Enforcement Timing (Strict)
Policies are evaluated at hard enforcement points.

| Stage               | Policies Evaluated      |
| ------------------- | ----------------------- |
| Before Silver write | Schema, Layer boundary  |
| Before Gold write   | Schema, PII, SLA, Layer |
| After write         | None (record only)      |

❗ No post-write policy checks


## 7. Enforcement Flow
```arduino
OpenLakeTx requests write
        ↓
LakeGuard evaluates policies
        ↓
Decision = ALLOW / BLOCK
        ↓
If BLOCK → write prevented
If ALLOW → write proceeds
```
This decision is authoritative


## 8. Policy Violation Behavior
| Scenario               | Outcome       |
| ---------------------- | ------------- |
| Single policy violated | Write blocked |
| Multiple violations    | Write blocked |
| Evaluation failure     | Write blocked |
| Unknown policy state   | Write blocked |

> Uncertainty defaults to safety

## 9. Recording Policy Decisions
Every evaluation is recorded.

#### Conceptual decisions fields
| Field        | Description          |
| ------------ | -------------------- |
| run_id       | Execution reference  |
| policy_id    | Evaluated policy     |
| result       | ALLOW / BLOCK        |
| evaluated_at | Timestamp            |
| reason       | Human-readable cause |

This enables:
- Audit
- RCA
- Compliance review
- E2E testing validation


## 10. Interaction with Quality Rules
Order of enforcement is intentional:
```markdown
1. Policy checks
2. Quality checks
3. Promotion decision
```
Reason:
- Policies may forbid *valid* data
- Quality never overrides policy


## 11. Interaction with Promotion Gates
Promotion requires:
- All applicable policies -> ALLOW
- All applicable quality rules -> PASS

if either fails:
- Promotion is blocked
- Status recorded
- Downstream layers halted


## 12. What Policy Enforcement Does Not Do
Explicit exclusions:
- Data masking
- Encryption
- Access control
- User authorization
- Remediation workflows

These belong to security and access planes, not Phase-1


## 13. Failure-First Design (Intentional)
Policies are designed to:
- Fail early
- Fail loud
- Fail deterministically

There is no override flag.

This is what makes the platform trustworthy.

## 14. Phase-1 Exit Criteria (Policy)
Policy enforcement is complete when:
- Policy types are defined
- Enforcement timing is explicit
- Violation behavior is deterministic
- Metadata recording is mandatory

## ✅ Canonical Policy Guarantee
> If data violates a platform policy, it does not exist -- regardless of pipeline success.

This is real governance, not documentation theater.
