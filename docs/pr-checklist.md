# Pull Request Checklist -- OpenLakeTx & LakeGuard Platform

**Purpose**
Ensure every change preserves the **lakehouse architecure, DataOps guarantees, and platform principle defined in the Architecture README.

**Rule**
If any mandatory item below is ❌, the PR must not be merged.

---

## 1. Architecture Alignment (Mandatory)
- [ ] This change aligns with the Architecture README
- [ ] Responsiblilities remain clearly separated:
    - [ ] Storage (GCS)
    - [ ] Transactions (OpenLakeTx)
    - [ ] Operations (LakeGuard)
    - [ ] Compute (Spark/SQL)
- [ ] Any deviation is documented in Design Decisions & Tradeoffs

---

## 2. OpenLakeTx -- Transactional Layer Checks
(Required if this PR touches data writes, metadata, or commits)
- [ ] Writes are atomic (no partial visibility)
- [ ] Commit metadata is append-only
- [ ] Snapshot versioning is preserved
- [ ] Rollback and retry behavior is deterministic
- [ ] Concurrency conflicts are handled explicitly
- [ ] No compute logic leaks into the transaction layer

---

## 3. LakeGuard -- DataOps & Trust Checks
(Required if this PR affects data quality, SLAs, or validation logic)
- [ ] Data quality rules are explicit and versioned
- [ ] Freshness / SLA expectations are defined
- [ ] Failure modes are classified (quality / infra / schema)
- [ ] Downstream propagation is blocked on failure
- [ ] Metrics are emitted for observability
- [ ] No best-effort or silent validation logic introduced

---

## 4. Medallion Layer Discipline

- [ ] Bronze is append-only and immutable
- [ ] Silver handles cleaning, validation, and conformance
- [ ] Gold contains business logic only
- [ ] No Gold logic leaks into Silver or Bronze
- [ ] Schema contracts between layers are documented



## 5. Failure-First Design

- [ ] Failure scenarios were explicitly considered
- [ ] Recovery paths are documented
- [ ] System behavior is deterministic after failure
- [ ] Retries are idempotent
- [ ] No silent failure paths exist

---

## 6. Data Quality as a Gate

- [ ] Bad data cannot reach downstream consumers
- [ ] Quality checks block, not just report
- [ ] Thresholds and tolerances are defined
- [ ] Data health status is persisted and auditable

---

## 7. Compute & Performance Considerations

- [ ] Spark jobs are idempotent
- [ ] Partitioning strategy is documented
- [ ] No hard-coded cluster assumptions
- [ ] Compute is decoupled from storage
- [ ] Performance tradeoffs are acknowledged

---

## 8. Security & Governance

- [ ] No credentials are committed
- [ ] IAM boundaries are respected
- [ ] Read vs Write premissions are explicit
- [ ] Metadata does not expose sensitive data
- [ ] Access-related changes are documented

---

## 9. Observability & Monitoring

- [ ] Metrics emitted (success, failure, latency)
- [ ] Logs are structured and actionable
- [ ] Alerts are meaningful (not noisy)
- [ ] Lineage impact is understood

---

## 10. Documentation & Contracts

- [ ] README updated if behavior changes
- [ ] Architecture docs referenced if applicable
- [ ] Design decision documented (if required)
- [ ] Public interfaces are versioned
- [ ] Breaking changes are clearly called out

---

## 11. Testing & Validation

- [ ] Unit tests cover core logic
- [ ] Failure scenarios are tested
- [ ] Idempotency is validated
- [ ] Schema evolution cases are tested
- [ ] Backward compatibility is verified

---

## 12. Author Declaration
- [ ] I have reviewed this change against the Architecture README
- [ ] I confirm this change does not weaken platform guarantees
- [ ] I understand the failure modes introduced by this PR


---

## 13. Notes (Required if Any Item is Unchecked)
```text
Explain:
- Why the deviation is acceptable
- What risk it introduces
- How the risk will be mitigated
```

---

## Non-Negotiable Rule

> If a PR violates platform guarantees, it must be rejected -- even if it "works".

--