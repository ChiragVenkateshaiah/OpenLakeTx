# 📘 Phase 1 - `log.py` Design Document

Project: OpenLakeTx
Layer: Core Infrastructure
Component: Logging Framework

---

## 1. Purpose of `log.py`
The `log.py` module provides a centralized, consistent, and extensible logging mechanism for the OpenLakeTx engine.

Its goal are to:

- Standardize logging across all components (`storage.py`, future `transaction.py`, `metadata.py`)
- Support debugging, auditability, and observability
- Be lightweight, dependency-free (initially), and configurable
- Mimic production-grade logging patterns used in data platforms (Delta Lake, Spark, Airflow)

---

## 2. Why Logging Is Critical in a Data Lake Engine
In real-world data platforms, logs are essential for:

| Area              | Why it Matters                                  |
| ----------------- | ----------------------------------------------- |
| Debugging         | Trace failures in file writes, metadata updates |
| Auditing          | Track who did what, when, and where             |
| Monitoring        | Detect performance bottlenecks                  |
| Compliance        | Maintain operational transparency               |
| Incident Response | Replay events leading to failures               |

> Logging is the backbone of observability in distributed data systems

---

## 3. Design Principles
The logging system should follow these principles:
1. Single Responsibility
    - `log.py` only handles logging logic
2. Centralized Control
    - All modules import the same logger
3. Configurable Levels
    - DEBUG, INFO, WARNING, ERROR, CRITICAL
4. Structured Messages
    - Timestamped, leveled, module-aware
5. Minimal Overhead
    - No heavy external dependencies initially

---

## 4. Functional Requirements

### 4.1 Logging Levels
The logger must support standard severity levels:
| Level    | Usage                                                  |
| -------- | ------------------------------------------------------ |
| DEBUG    | Internal state, development debugging                  |
| INFO     | High-level operations (file created, commit completed) |
| WARNING  | Non-fatal issues                                       |
| ERROR    | Failed operations                                      |
| CRITICAL | System-breaking errors                                 |

---

### 4.2 Output Destinations
#### Phase 1 scope:
- ✅ Console (stdout)
- ✅ File-based logging (`logs/openlaketx.log`)

#### Future phases (not implemented yet):
- Cloud logging (GCP/Azure)
- JSON structured logs
- Centralized log aggregation

---

### 4.3 Log Format (Initial)
Each log entry should include:
```css
[TIMESTAMP] [LEVEL] [MODULE] message
```
Example:
```pgsql
2026-01-13 11:45:02 | INFO | storage | Bronze file written successfully
```

---

## 5. Public API Design
`log.py` should expose simple and intuitive functions

### 5.1 Logger Initialization
```python
get_logger(name: str) -> Logger
```
#### Responsibilities:
- Create or reuse a logger instance
- Attach handlers (console + file)
- Apply formatter
- Prevent duplicate handlers

---

### 5.2 Logging Usage Pattern
Example usage from another module (`storage.py`)
```python
from core.log import get_logger

logger = get_logger(__name__)

logger.info("Storage layer initialized")
logger.error("Failed to write data file")
```
---

## 6. Internal Architecture
### 6.1 Components
| Component | Responsibility                |
| --------- | ----------------------------- |
| Logger    | Main logging interface        |
| Handler   | Determines where logs go      |
| Formatter | Defines log message structure |

### 6.2 Handler Strategy
- StreamHandler
    - Writes logs to console
- FileHandler
    - Writes logs to disk
    - Auto-create `logs/` directory if missing

---

## 7. Error Handling Strategy
`log.py` must never crash the application.

### Rules:
- Logging failures should fail silently or fallback to console
- File permission issues should not stop execution
- Defensive checks around handler creation

---

## 8. Testing Strategy (Planned)

Before integration:
- Verify logger creation does not duplicate handlers
- Confirm logs appear in:
    - Console
    - Log file
- Validate log level filtering
- Ensure multiple modules can use the same logger safely

---

## 9. Phase-wise Evolution Plan
| Phase   | Enhancements                     |
| ------- | -------------------------------- |
| Phase 1 | Basic console + file logging     |
| Phase 2 | JSON logs                        |
| Phase 3 | Correlation IDs (transaction_id) |
| Phase 4 | Cloud-native logging             |
| Phase 5 | Metrics + tracing integration    |
