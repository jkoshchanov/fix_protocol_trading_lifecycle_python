# FIX Protocol Trading Lifecycle — Python

An SDET-focused test automation project that validates trading orders using the **FIX 4.2 protocol**. Built with [`simplefix`](https://github.com/da4089/simplefix) (free, open-source) and `pytest`.

---

## What This Project Covers

Full trading order lifecycle validation:

| Step | FIX Message | MsgType |
|------|-------------|---------|
| Place order | NewOrderSingle | `35=D` |
| Broker acknowledgement | ExecutionReport (New) | `35=8` |
| Partial fill | ExecutionReport (PartialFill) | `35=8` |
| Full fill | ExecutionReport (Fill) | `35=8` |
| Cancel order | OrderCancelRequest | `35=F` |
| Modify order | OrderCancelReplaceRequest | `35=G` |
| Query status | OrderStatusRequest | `35=H` |
| Cancel rejected | OrderCancelReject | `35=9` |

---

## Project Structure

```
fix_protocol_trading_lifecycle_python/
├── fix_messages/
│   ├── __init__.py
│   └── constants.py        # FIX tag numbers, MsgType, OrdType, Side, etc.
├── validators/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| `simplefix` | Build and encode/decode FIX protocol messages |
| `pytest` | Test runner and assertions |
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

# Run a specific test file
pytest tests/test_trading_lifecycle.py -v
```

---

## Key FIX Tags Used

| Tag | Name | Description |
|-----|------|-------------|
| 8 | BeginString | Protocol version (`FIX.4.2`) |
| 11 | ClOrdID | Client-assigned order ID |
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

