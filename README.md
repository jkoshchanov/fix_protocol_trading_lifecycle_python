# FIX Protocol Trading Lifecycle — Python

[![Tests](https://github.com/jkoshchanov/fix_protocol_trading_lifecycle_python/actions/workflows/tests.yml/badge.svg)](https://github.com/jkoshchanov/fix_protocol_trading_lifecycle_python/actions/workflows/tests.yml)

An SDET-focused test automation project that validates trading orders using the **FIX 4.2 protocol**. Built with [`simplefix`](https://github.com/da4089/simplefix) (free, open-source) and `pytest`.

---

## What This Project Covers

Full trading order lifecycle validation, including quantity bookkeeping (CumQty + LeavesQty = OrderQty) and the volume-weighted average fill price (AvgPx):

| Step | FIX Message | MsgType |
|------|-------------|---------|
| Place order | NewOrderSingle | `35=D` |
| Broker acknowledgement | ExecutionReport (New) | `35=8` |
| Partial fill | ExecutionReport (PartialFill) | `35=8` |
| Full fill | ExecutionReport (Fill) | `35=8` |
| Cancel order | OrderCancelRequest | `35=F` |
| Modify order | OrderCancelReplaceRequest | `35=G` |
| Cancel rejected | OrderCancelReject | `35=9` |

---

## Project Structure

```
fix_protocol_trading_lifecycle_python/
├── features/
│   ├── new_order.feature           # 3 scenarios — NewOrderSingle (35=D)
│   ├── execution_report.feature    # 4 scenarios — ExecutionReport (35=8)
│   ├── order_cancel.feature        # 2 scenarios — Cancel request & reject
│   ├── order_replace.feature       # 1 scenario  — Cancel/replace (35=G)
│   └── trading_lifecycle.feature   # 3 end-to-end lifecycle scenarios
├── fix_messages/
│   ├── __init__.py
│   ├── constants.py        # FIX tag numbers, MsgType, OrdType, Side, etc.
│   └── message_builder.py  # Builders for each FIX message type
├── validators/
│   ├── __init__.py
│   └── fix_validator.py    # Field-level assertions and lifecycle validators
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # All Given/When/Then steps + context fixture
│   ├── test_new_order.py           # Loads new_order.feature scenarios
│   ├── test_execution_report.py    # Loads execution_report.feature scenarios
│   ├── test_order_cancel.py        # Loads order_cancel.feature scenarios
│   ├── test_order_replace.py       # Loads order_replace.feature scenarios
│   └── test_trading_lifecycle.py   # Loads trading_lifecycle.feature scenarios
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| `simplefix` | Build and encode/decode FIX protocol messages |
| `pytest` | Test runner and assertions |
| `pytest-bdd` | Gherkin BDD support (Feature / Scenario / Given / When / Then) |
| `pytest-html` | HTML test report generation |

---

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with HTML report
pytest tests/ -v --html=report.html --self-contained-html

# Run a specific feature
pytest tests/test_trading_lifecycle.py -v

# Run with BDD scenario names visible
pytest tests/ -v --no-header -rN
```

---

## Key FIX Tags Used

| Tag | Name | Description |
|-----|------|-------------|
| 6 | AvgPx | Average price of all fills (quantity-weighted) |
| 8 | BeginString | Protocol version (`FIX.4.2`) |
| 11 | ClOrdID | Client-assigned order ID |
| 14 | CumQty | Total quantity filled so far |
| 35 | MsgType | Message type identifier |
| 37 | OrderID | Broker-assigned order ID |
| 38 | OrderQty | Order quantity |
| 39 | OrdStatus | Order status |
| 40 | OrdType | Order type (Market, Limit, etc.) |
| 44 | Price | Limit price |
| 49 | SenderCompID | Sender identifier |
| 54 | Side | Buy / Sell |
| 55 | Symbol | Instrument ticker |
| 150 | ExecType | Execution type |
| 151 | LeavesQty | Remaining open quantity |

---

## Continuous Integration

GitHub Actions runs the full suite on every push and pull request to `main` (`.github/workflows/tests.yml`) and saves the HTML report as a downloadable artifact.

---

## BDD Approach

Tests are written in **Gherkin syntax** using `pytest-bdd`:

- `.feature` files in `features/` define scenarios in plain English (Feature / Scenario / Given / When / Then)
- Step definitions in `tests/conftest.py` map each Gherkin step to Python code
- Test files (`test_*.py`) are single-line files that load their feature file via `scenarios()`
- All steps are registered in `conftest.py` so they are shared across all feature files without duplication

---

## AI Assistance Note

Project configuration, environment setup, and scaffolding were done with AI assistance.
The actual test scripting and validation logic in Python is authored manually without AI involvement.

