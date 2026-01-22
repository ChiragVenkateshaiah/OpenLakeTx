# Contributing to OpenLakeTx + LakeGuard

Thank you for your interest in contributing to this repository.

This project is a platform-first data lakehouse, not a collection of ad-hoc pipelines.
All contributions must preserve transactional safety, DataOps guarantees, and architectural discipline.

---

## 🧭 Guiding Principles

Before contributing, understand these non-negotiable principles:

- Platform guarantees > feature velocity
- Architecture is enforced, not implied
- Failures are expected and designed for
- Pipelines are replaceable; platform guarantees are not

If a change violates these principles, it will be rejected — even if it “works”.

---

## 📚 Required Reading (Mandatory)

All contributors must review the following documents before making changes:

- Architecture Overview
    → docs/architecture.md

- Design Decisions & Tradeoffs
    → docs/design-decisions.md

- Pull Request Checklist (Governance Contract)
    → docs/pr-checklist.md

These documents define how the platform must behave.

---

## 🏗️ Understanding the Repository Structure

Contributors are expected to respect ownership boundaries:

- openlaketx/ → Transaction & control plane
- lakeguard/ → DataOps, quality, SLAs, trust
- pipelines/ → Compute logic only (Bronze / Silver / Gold)
- infra/ → GCP infrastructure & orchestration
- docs/ → Canonical platform contracts

Cross-boundary logic is explicitly disallowed unless documented as a design decision.


---

🔁 Contribution Workflow
1. Create a Branch

Create a feature branch from main:
```bash
git checkout -b feature/<short-description>
```

2. Make Changes with Architecture in Mind

While implementing changes:

- Assume failures will occur
- Preserve idempotency and determinism
- Avoid embedding guarantees inside pipelines
- Keep compute, control, and ops concerns separated

3. Open a Pull Request (Mandatory Checklist)

When opening a PR:

- GitHub will automatically load the PR Checklist
from .github/pull_request_template.md
- All relevant checklist items must be completed
- Any unchecked item must be justified

> The PR checklist is a merge gate, not a formality.


4. Review & Merge Rules

A PR must not be merged if:

- It violates the Architecture README
- It weakens transactional or DataOps guarantees
- It introduces silent failure paths
- It bypasses quality or SLA enforcement
- It creates architectural drift

---

## ✅ Pull Request Governance

All PRs are governed by:

- PR Template (enforced)
    → .github/pull_request_template.md

- Canonical Checklist (reference)
    → docs/pr-checklist.md

If there is a conflict between:

- Code vs
- Architecture / Checklist

👉 Architecture wins

---

## 🧪 Testing Expectations

Depending on the area touched, contributors should ensure:

- Transaction logic is deterministic and idempotent
- Failure scenarios are explicitly tested
- Schema evolution is backward compatible
- Quality gates behave as blocking mechanisms
- Observability signals are emitted
- Tests should focus on failure behavior, not just the happy path.

---

## 📐 Design Changes & Tradeoffs

If a change introduces a new architectural decision:

1. Document it in docs/design-decisions.md
2. Clearly explain:
    - Why the change is needed
    - What alternatives were considered
    - What tradeoffs are accepted

Undocumented design changes will be rejected.


---

.

## 🔒 Security & Governance Rules

- Do not commit credentials or secrets
- Respect IAM and access boundaries
- Metadata must not expose sensitive data
- Access changes must be documented

---


## 🛑 Non-Goals (Important)

This repository does not aim to:

- Optimize for fastest delivery
- Demonstrate every GCP service
- Replace mature OSS lakehouse engines
- Serve as a low-level ETL tutorial

It exists to demonstrate how data platforms are designed and governed.

---

## 🧠 Contributor Declaration (Implicit)

By opening a PR, you acknowledge that:
- You have reviewed the architecture
- You understand the platform guarantees
- You accept that correctness > convenience
- You are comfortable having a PR rejected for architectural reasons

---

## 🔗 Reference Links

- Architecture → docs/architecture.md
- Design Decisions → docs/design-decisions.md
- PR Checklist → docs/pr-checklist.md

---

## 📌 Final Rule

> If a change violates platform guarantees, it must not be merged — even if it passes tests.