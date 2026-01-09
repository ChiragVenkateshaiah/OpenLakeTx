# OpenLakeTx - Architecture & Design

OpenLakeTx is a minimal, educational implementation of a Delta Lake-style transactional data lake, built in python on top of open-source technologies.

This document explains:
- The folder structure
- The responsibilities of each module
- Why each dependency was chosen

---

## 📁 Project Folder Structure

```text
openlaketx/
├── openlaketx/
│   ├── __init__.py
│   ├── table.py
│   ├── commit.py
│   ├── log.py
│   ├── snapshot.py
│   ├── storage.py
│   └── gc.py
├── cli/
│   └── main.py
├── tests/
├── examples/
├── README.md
├── ARCHITECTURE.md
└── pyproject.toml
```

---

## Core Package: `openlaketx/`
This directory contains the **core engine** and is published as a Python package.

### `table.py` - **Public API Layer**
- Entry point for users
- Exposes high-level operations such as:
    - create table
    - write data
    - read data
    - time travel
- Abstracts away transaction logs and storage details
> Similiar to `DeltaTable` in Delta Lake

---

### `commit.py` - **Transaction Logic**
- Handles wrtie transactions
- Responsible for:
    - optimistic concurrency control
    - atomic commits
    - version assignment
- Ensures ACID-like guarantees on object storage

---

### `log.py` - **Transaction Log Management**
- Reads and writes `_delta_log`-style JSON files
- Stores actions such as:
    - `add`
    - `remove`
    - `metadata`
- Forms the **source of truth** for the table state

---

### `snapshot.py` **- Read Path & Version Resolution**
- Computes table state at a given version
- Merges log actions into a consistent snapshot
- Supports:
    - latest reads
    - time travel reads

---

### `storage.py` - **Storage Abstraction Layer**
- Abstracts filesystem operations
- Currently supports:
    - Google Cloud Storage (GCS)
- Designed to be extensible for:
    - local filesystem
    - AWS S3
    - Azure Blob Storage
> Keeps business logic independent of storage backend

---

### `gc.py` - **Garbage Collection (VACUUM)**
- Identifies unreferenced Parquet files
- Deletes old data safely
- Mimics Delta Lake's `VACUUM` behavior

---
## CLI Layer: `cli/`
### `cli/main.py`
- Command-line interface for OpenLakeTx
- Built using Typer
- Planned commands:
    -`openlaketx init`
    -`openlaketx history`
    -`openlaketx vacuum`

---

## Testing: `test/`
- Unit tests for:
    - commits
    - snapshots
    - conflict detection
- Integration tests using local or GCS-backed storage
- Uses `pytest`

---

## Examples: `examples/`
- End-to-end usage examples
- Demo scripts and notebooks
- Useful for:
    - learning
    - documentation
    - quick validation

---

## Dependency Choices & Rationale
### Core Data & Storage
| Dependency    | Reason                                                     |
| ------------- | ---------------------------------------------------------- |
| `pyarrow`     | Columnar data model, Parquet IO, schema handling           |
| `pandas`      | Developer-friendly data creation and testing               |
| `gcsfs`       | Native filesystem interface for Google Cloud Storage       |
| `fastparquet` | Alternative Parquet writer for performance & compatibility |

---

## Developer Experience
| Dependency | Reason                              |
| ---------- | ----------------------------------- |
| `pytest`   | Reliable unit & integration testing |
| `typer`    | Modern, type-safe CLI creation      |
| `rich`     | Human-friendly terminal output      |

---

## Design Principles
- Log-first architecture
- Immutable data files
- Append-only transaction log
- Storage-agnostic design
- Minimal but extensible

---

## Open Source Stack (Zero Cost)
| Layer       | Choice                | Why                    |
| ----------- | --------------------- | ---------------------- |
| Language    | Python 3.10+          | Fast iteration         |
| Storage     | Google Cloud Storage  | Object-store semantics |
| File format | Parquet               | Columnar, standard     |
| Metadata    | JSON → SQLite (later) | Simplicity             |
| CLI         | argparse / typer      | Clean UX               |
| Tests       | pytest                | Confidence             |
| Formatting  | black + ruff          | Professional           |
| Packaging   | poetry / pip          | Clean deps             |

---

## Future Enhancements
- Schema evolution
- Z-order / data skipping
- Streaming commits
- S3 & Azure Blob support
- Table-level metrics

---

## Summary
OpenLakeTx is designed to demonstrate a deep understanding of:
- data lake internals
- transactional systems
- real-world data engineering design

