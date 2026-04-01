"""
FIX message validators with assertion helpers.
Each method raises AssertionError with a descriptive message on failure.
"""
import simplefix
from fix_messages.constants import Tag, MsgType


def get_field(msg: simplefix.FixMessage, tag: int) -> bytes:
    """Return the raw bytes value of a tag, or raise if missing."""
    value = msg.get(tag)
    assert value is not None, f"Tag {tag} is missing from message"
    return value


def assert_msg_type(msg: simplefix.FixMessage, expected: bytes) -> None:
    actual = get_field(msg, Tag.MsgType)
    assert actual == expected, (
        f"MsgType mismatch: expected {expected!r}, got {actual!r}"
    )


def assert_field_equals(msg: simplefix.FixMessage, tag: int, expected, label: str = "") -> None:
    actual = get_field(msg, tag)
    if isinstance(expected, str):
        expected = expected.encode()
    assert actual == expected, (
        f"Tag {tag} ({label}) mismatch: expected {expected!r}, got {actual!r}"
    )


def assert_field_present(msg: simplefix.FixMessage, *tags: int) -> None:
    for tag in tags:
        get_field(msg, tag)  # raises if missing


def assert_numeric_gte(msg: simplefix.FixMessage, tag: int, minimum: float, label: str = "") -> None:
    raw = get_field(msg, tag)
    value = float(raw)
    assert value >= minimum, (
        f"Tag {tag} ({label}) value {value} is less than minimum {minimum}"
    )


def assert_numeric_lte(msg: simplefix.FixMessage, tag: int, maximum: float, label: str = "") -> None:
    raw = get_field(msg, tag)
    value = float(raw)
    assert value <= maximum, (
        f"Tag {tag} ({label}) value {value} exceeds maximum {maximum}"
    )


def assert_numeric_equals(msg: simplefix.FixMessage, tag: int, expected: float,
                          label: str = "", tolerance: float = 0.0001) -> None:
    raw = get_field(msg, tag)
    actual = float(raw)
    assert abs(actual - expected) <= tolerance, (
        f"Tag {tag} ({label}) expected {expected}, got {actual}"
    )


# ---------------------------------------------------------------------------
# Lifecycle-level validators
# ---------------------------------------------------------------------------

def validate_new_order_single(msg: simplefix.FixMessage, cl_ord_id: str,
                               symbol: str, side: bytes) -> None:
    """Assert all mandatory fields of a NewOrderSingle are correct."""
    assert_msg_type(msg, MsgType.NewOrderSingle)
    assert_field_present(msg, Tag.ClOrdID, Tag.HandlInst, Tag.Symbol,
                         Tag.Side, Tag.TransactTime, Tag.OrderQty, Tag.OrdType)
    assert_field_equals(msg, Tag.ClOrdID, cl_ord_id, "ClOrdID")
    assert_field_equals(msg, Tag.Symbol, symbol, "Symbol")
    assert_field_equals(msg, Tag.Side, side, "Side")
    assert_field_equals(msg, Tag.BeginString, b"FIX.4.2", "BeginString")
    assert_numeric_gte(msg, Tag.OrderQty, 0.0001, "OrderQty")


def validate_execution_report(msg: simplefix.FixMessage, expected_ord_status: bytes,
                               expected_exec_type: bytes, cl_ord_id: str) -> None:
    """Assert mandatory ExecutionReport fields and status/type match."""
    assert_msg_type(msg, MsgType.ExecutionReport)
    assert_field_present(msg, Tag.OrderID, Tag.ExecID, Tag.ExecType,
                         Tag.OrdStatus, Tag.LeavesQty, Tag.CumQty, Tag.AvgPx)
    assert_field_equals(msg, Tag.OrdStatus, expected_ord_status, "OrdStatus")
    assert_field_equals(msg, Tag.ExecType, expected_exec_type, "ExecType")
    assert_field_equals(msg, Tag.ClOrdID, cl_ord_id, "ClOrdID")
    assert_numeric_gte(msg, Tag.CumQty, 0, "CumQty")
    assert_numeric_gte(msg, Tag.LeavesQty, 0, "LeavesQty")


def validate_fill_quantities(msg: simplefix.FixMessage, total_qty: float) -> None:
    """Assert CumQty + LeavesQty == OrderQty for an ExecutionReport."""
    cum_qty = float(get_field(msg, Tag.CumQty))
    leaves_qty = float(get_field(msg, Tag.LeavesQty))
    assert abs((cum_qty + leaves_qty) - total_qty) < 0.0001, (
        f"Quantity mismatch: CumQty({cum_qty}) + LeavesQty({leaves_qty}) "
        f"!= OrderQty({total_qty})"
    )


def validate_order_cancel_request(msg: simplefix.FixMessage, cl_ord_id: str,
                                   orig_cl_ord_id: str, symbol: str) -> None:
    """Assert mandatory OrderCancelRequest fields."""
    assert_msg_type(msg, MsgType.OrderCancelRequest)
    assert_field_present(msg, Tag.OrigClOrdID, Tag.ClOrdID,
                         Tag.Symbol, Tag.Side, Tag.TransactTime)
    assert_field_equals(msg, Tag.ClOrdID, cl_ord_id, "ClOrdID")
    assert_field_equals(msg, Tag.OrigClOrdID, orig_cl_ord_id, "OrigClOrdID")
    assert_field_equals(msg, Tag.Symbol, symbol, "Symbol")


def validate_order_cancel_replace(msg: simplefix.FixMessage, cl_ord_id: str,
                                   orig_cl_ord_id: str, new_qty: float) -> None:
    """Assert mandatory OrderCancelReplaceRequest fields."""
    assert_msg_type(msg, MsgType.OrderCancelReplaceRequest)
    assert_field_present(msg, Tag.OrigClOrdID, Tag.ClOrdID, Tag.HandlInst,
                         Tag.Symbol, Tag.Side, Tag.OrdType, Tag.TransactTime)
    assert_field_equals(msg, Tag.ClOrdID, cl_ord_id, "ClOrdID")
    assert_field_equals(msg, Tag.OrigClOrdID, orig_cl_ord_id, "OrigClOrdID")
    assert_numeric_equals(msg, Tag.OrderQty, new_qty, "OrderQty")


def validate_order_cancel_reject(msg: simplefix.FixMessage, cl_ord_id: str) -> None:
    """Assert mandatory OrderCancelReject fields."""
    assert_msg_type(msg, MsgType.OrderCancelReject)
    assert_field_present(msg, Tag.OrderID, Tag.ClOrdID,
                         Tag.OrigClOrdID, Tag.OrdStatus, Tag.Text)
    assert_field_equals(msg, Tag.ClOrdID, cl_ord_id, "ClOrdID")
