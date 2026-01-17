## 12. Design Decisions & Tradeoffs
This section documents intentional architectural choices, alternatives considered, and the tradeoffs involved.
Its purpose is to make reasoning explicit and prevent future misinterpretation of the system design.


### 12.1 Object Storage as the System of Record
#### Decision
Use **Google Cloud Storage** as the primary system of record.

#### Alternatives Considered
- Using **BiQuery** as primary storage
- Using a traditional RDBMS

#### Why this decision
- Object storage is cheap, durable, and infinitely scalable
- Enables open table formats and engine independence
- Decouples storage from compute

#### Tradeoffs
- Requires a transaction layer (solved by OpenLakeTx)
- Higher operational complexity than managed warehouse

---

### 12.2 Custom Transaction Layer (OpenLakeTx)

#### Decision
Build and use OpenLakeTx as a standalone transaction & control plane.

#### Alternatives Considered
- Using Delta Lake / Iceberg directly
- Delegating consistency to compute engines

#### Why This Decision
- Demonstrates deep understanding of lakehouse internals
- Allows fine-grained control over commit semantics
- Enables engine-agnostic design

#### Tradeoffs
- Higher implementation complexity
- Requires rigorous testing and validation
- Not a drop-in replacement for mature OSS yet

---

### 12.3 Separation of Transaction and DataOps Planes
#### Decision
Separate transaction safety (OpenLakeTx) from data trust & operations (LakeGuard)

#### Alternative Considered
- Embedding quality checks inside Spark jobs
- Relying on downstream consumers to validate data

#### Why This Decision
- Clean separation of concerns
- Allows independent evolution of reliability and observability
- Matches real-world platform team structures

#### Tradeoffs
- Requires orchestration coordination
- Adds an additional platform component

---

### 12.4 Medallion Architecture (Bronze/Silver/Gold)
#### Decision
Adopt a Medallion Architecture layered on top of the lakehouse

#### Alternative Considered
- Single-layer lake
- Domain-specific marts only

#### Why This Decision
- Clear data contracts between layers
- Easier debugging and rollback
- Enables incremental quality enforcement

#### Tradeoffs
- Data duplication across layers
- Requires discipline in enforcing boundaries

---

### 12.5 Spark as Primary Compute Engine
#### Decision
Use **Dataproc** (Spark) for batch & transformations.

#### Alternatives Considered
- SQL-only pipelines
- Custom Python processing
- Managed ETL tools

#### Why This Decision
- Mature ecosystem
- Handles large-scale batch and streaming
- Integrates naturally with object storage

#### Tradeoffs
- Requires cluster management
- Slower startup times vs serverless SQL

---

### 12.6 BigQuery as a Customer, Not Owner
#### Decision
Position **BigQuery** as a read/query layer, not the storage owner.

#### Alternatives Considered
- Using BigQuery-managed storage
- Fully warehouse-centric architecture

#### Why This Decision
- Prevents vendor lock-in
- Preserves open data access
- Enables multiple compute engines

#### Tradeoffs
- Requires external table or ingestion setup
- Sightly higher query latency for external reads

---

### 12.7 Explicit Failure Handling Over "Happy Path"
#### Decision
Design every pipeline assuming failures are normal

#### Alternative Considered
- Best-effort ETL pipelines
- Manual recovery processes

#### Why This Decision
- Reflects production realities
- Enables deterministic recovery
- Improves system trust

#### Tradeoffs
- More upfront engineering effort
- Requires disciplined observability

---

### 12.8 Data Quality as a Gate, Not a Report
#### Decision
LakeGuard enforces quality as a blocking gate, not a passive dashboard.

#### Alternative Considered
- Post-hoc data quality reports
- BI-level validation

#### Why This Decision
- Prevents bad data from propagating
- Makes failures visible early
- Aligns with DataOps best practices

#### Tradeoffs
- Pipelines may halt more often
- Requires well-defined SLAs and thresholds

---

### 12.9 Open Formats Over Proprietary Systems
#### Decisions
Use open file formats (Parquet + metadata logs).

#### Alternative Considered
- Proprietary warehouse formats
- Closed vendor-specific engines

#### Why This Decision
- Long-term sustainability
- Interoperability
- Auditability and portability

#### Tradeoffs
- Some performance optimizations require manual tuning
- More responsibility on platform engineering

---

### 12.10 Platform-First, Pipeline-Second Mindset
#### Decision
Build a platform before building many pipelines

#### Alternatives Considered
- Direct ETL pipeline focus
- Tool-first approach

#### Why This Decision
- Scales across teams and domains
- Reduces duplicated logic
- Encourages standards and reuse

### Tradeoffs
- Slower initial feature velocity
- Higher upfront design investment

---

## 13. Architectural North Star
> If the platform guarantees correctness, reliability, and observability, pipelines become replaceable

This principle guides all future evolution of OpenLakeTx and LakeGuard
