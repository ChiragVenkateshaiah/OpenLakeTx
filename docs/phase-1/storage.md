# Phase 1 – Storage Layer (storage.py)

## Overview

The storage layer is the lowest-level component in OpenLakeTx.
It provides a thin abstraction over the local filesystem and is intentionally kept simple.

This layer is implemented in `openlaketx/storage.py`.

**Phase 1 focuses only on the write path**, so the storage layer is responsible for:
- Directory creation
- File read/write
- File existence checks
- Listing files deterministically

No transactional or table-level logic exists at this layer.

---

## Design Philosophy

The storage layer follows these principles:

- **Dumb but reliable**: No business logic
- **Filesystem-only responsibility**
- **Idempotent operations**
- **Deterministic behavior**

All higher-level concepts such as:
- Table semantics
- Transaction logs
- Versioning
- Concurrency

are handled in upper layers (`log.py`, `commit.py`).

---

## Responsibilities of storage.py

### What it does

- Creates directories safely
- Writes files to disk
- Reads files from disk
- Lists files in sorted order
- Checks existence of files or directories

### What it does NOT do

- Transaction management
- Version handling
- JSON commit logic
- Snapshot or read logic
- Concurrency control

---

## Implementation Details

### Base Path Isolation

Each `Storage` instance is initialized with a base path:

```python
Storage("./warehouse")
```
All file operations are scoped within this base path to avoid accidental writes outside the project directory

---
## Path Resolution
The `resolve()` method ensures that:
- Relative paths are resolved against the base path
- Absolute paths are respected as-is

This guarantees consistent and safe path handling across the system

---
## Directory Creation
Directories are created using:
- `parents=True` to create intermediate directories
- `exist_ok=True` to ensure idempotency
This allows repeated execution without failures

---
## File Operations
- Files are written using standard write mode
- Parent directories are auto-created if missing
- Reading a missing file raises a clear error

Atomicity is not handled at this layer and is delegated to the commit protocol

---

## File Listing
Files are:
- Filtered to exclude directories
- Sorted lexicographically

Deterministic ordering is critical for future transaction log versioning

---

## Manual Testing (Initial Validation)
The storage layer was tested manually using Python REPL

### Step 1: Initialize Storage
```python
from openlaketx.storage import storage
s = Storage("./warehouse")
```

---

### Step 2: Create Directory
```python
s.mkdir("users/data")
```
Expected Result:
```bash
warehouse/users/data/
```

### Step 3: Write a File
```python
s.write_file("users/data/part-0001.txt", "hello world")
```

### Step 4: List files
```python
s.list_files("users/data")
```
Expected Output:
```text
['part-0001.txt']
```

### Step 5: Read File
```python
s.read_file("users/data/part-0001.txt")
```
Expected Output:
```text
hello world
```
---
## Outcome
The storage layer behaves as expected:
- All operations are deterministic
- No side effects or hidden logic
- Ready to support transactional layers in Phase 1

This completes the storage foundation for OpenLakeTx