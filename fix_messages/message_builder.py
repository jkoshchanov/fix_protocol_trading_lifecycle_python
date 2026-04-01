"""
Builders for common FIX 4.2 message types used in trading lifecycle tests.
Each builder returns a simplefix.FixMessage with all mandatory fields populated.
"""
import simplefix
from datetime import datetime, timezone
from fix_messages.constants import Tag, MsgType, HandlInst


def _utc_now() -> bytes:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H:%M:%S").encode()


def _base_header(msg: simplefix.FixMessage, msg_type: bytes, seq_num: int = 1,
                 sender: str = "CLIENT", target: str = "BROKER") -> None:
    msg.append_pair(Tag.BeginString, b"FIX.4.2")
    msg.append_pair(Tag.MsgType, msg_type)
    msg.append_pair(Tag.SenderCompID, sender.encode())
    msg.append_pair(Tag.TargetCompID, target.encode())
    msg.append_pair(Tag.MsgSeqNum, str(seq_num).encode())
    msg.append_pair(Tag.SendingTime, _utc_now())


def build_new_order_single(
    cl_ord_id: str,
    symbol: str,
    side: bytes,
    order_qty: float,
    ord_type: bytes,
    price: float = None,
    time_in_force: bytes = b"0",
    account: str = "ACC001",
    seq_num: int = 1,
) -> simplefix.FixMessage:
    """Build a NewOrderSingle (35=D) message."""
    msg = simplefix.FixMessage()
    _base_header(msg, MsgType.NewOrderSingle, seq_num)
    msg.append_pair(Tag.ClOrdID, cl_ord_id.encode())
    msg.append_pair(Tag.HandlInst, HandlInst.AutomatedNoIntervention)
    msg.append_pair(Tag.Symbol, symbol.encode())
    msg.append_pair(Tag.Side, side)
    msg.append_pair(Tag.TransactTime, _utc_now())
    msg.append_pair(Tag.OrderQty, str(order_qty).encode())
    msg.append_pair(Tag.OrdType, ord_type)
    if price is not None:
        msg.append_pair(Tag.Price, f"{price:.4f}".encode())
    msg.append_pair(Tag.TimeInForce, time_in_force)
    msg.append_pair(Tag.Account, account.encode())
    return msg


def build_execution_report(
    order_id: str,
    cl_ord_id: str,
    exec_id: str,
    exec_type: bytes,
    ord_status: bytes,
    symbol: str,
    side: bytes,
    leaves_qty: float,
    cum_qty: float,
    avg_px: float,
    last_qty: float = 0.0,
    last_px: float = 0.0,
    text: str = "",
    seq_num: int = 2,
) -> simplefix.FixMessage:
    """Build an ExecutionReport (35=8) message."""
    msg = simplefix.FixMessage()
    _base_header(msg, MsgType.ExecutionReport, seq_num, sender="BROKER", target="CLIENT")
    msg.append_pair(Tag.OrderID, order_id.encode())
    msg.append_pair(Tag.ClOrdID, cl_ord_id.encode())
    msg.append_pair(Tag.ExecID, exec_id.encode())
    msg.append_pair(Tag.ExecType, exec_type)
    msg.append_pair(Tag.OrdStatus, ord_status)
    msg.append_pair(Tag.Symbol, symbol.encode())
    msg.append_pair(Tag.Side, side)
    msg.append_pair(Tag.LeavesQty, str(leaves_qty).encode())
    msg.append_pair(Tag.CumQty, str(cum_qty).encode())
    msg.append_pair(Tag.AvgPx, f"{avg_px:.4f}".encode())
    msg.append_pair(Tag.LastQty, str(last_qty).encode())
    msg.append_pair(Tag.LastPx, f"{last_px:.4f}".encode())
    msg.append_pair(Tag.TransactTime, _utc_now())
    if text:
        msg.append_pair(Tag.Text, text.encode())
    return msg


def build_order_cancel_request(
    cl_ord_id: str,
    orig_cl_ord_id: str,
    symbol: str,
    side: bytes,
    order_qty: float,
    seq_num: int = 3,
) -> simplefix.FixMessage:
    """Build an OrderCancelRequest (35=F) message."""
    msg = simplefix.FixMessage()
    _base_header(msg, MsgType.OrderCancelRequest, seq_num)
    msg.append_pair(Tag.OrigClOrdID, orig_cl_ord_id.encode())
    msg.append_pair(Tag.ClOrdID, cl_ord_id.encode())
    msg.append_pair(Tag.Symbol, symbol.encode())
    msg.append_pair(Tag.Side, side)
    msg.append_pair(Tag.OrderQty, str(order_qty).encode())
    msg.append_pair(Tag.TransactTime, _utc_now())
    return msg


def build_order_cancel_replace_request(
    cl_ord_id: str,
    orig_cl_ord_id: str,
    symbol: str,
    side: bytes,
    order_qty: float,
    ord_type: bytes,
    price: float = None,
    seq_num: int = 3,
) -> simplefix.FixMessage:
    """Build an OrderCancelReplaceRequest (35=G) message."""
    msg = simplefix.FixMessage()
    _base_header(msg, MsgType.OrderCancelReplaceRequest, seq_num)
    msg.append_pair(Tag.OrigClOrdID, orig_cl_ord_id.encode())
    msg.append_pair(Tag.ClOrdID, cl_ord_id.encode())
    msg.append_pair(Tag.HandlInst, HandlInst.AutomatedNoIntervention)
    msg.append_pair(Tag.Symbol, symbol.encode())
    msg.append_pair(Tag.Side, side)
    msg.append_pair(Tag.OrderQty, str(order_qty).encode())
    msg.append_pair(Tag.OrdType, ord_type)
    if price is not None:
        msg.append_pair(Tag.Price, f"{price:.4f}".encode())
    msg.append_pair(Tag.TransactTime, _utc_now())
    return msg


def build_order_status_request(
    cl_ord_id: str,
    symbol: str,
    side: bytes,
    seq_num: int = 4,
) -> simplefix.FixMessage:
    """Build an OrderStatusRequest (35=H) message."""
    msg = simplefix.FixMessage()
    _base_header(msg, MsgType.OrderStatusRequest, seq_num)
    msg.append_pair(Tag.ClOrdID, cl_ord_id.encode())
    msg.append_pair(Tag.Symbol, symbol.encode())
    msg.append_pair(Tag.Side, side)
    return msg


def build_order_cancel_reject(
    order_id: str,
    cl_ord_id: str,
    orig_cl_ord_id: str,
    ord_status: bytes,
    text: str = "Order not found",
    seq_num: int = 4,
) -> simplefix.FixMessage:
    """Build an OrderCancelReject (35=9) message."""
    msg = simplefix.FixMessage()
    _base_header(msg, MsgType.OrderCancelReject, seq_num, sender="BROKER", target="CLIENT")
    msg.append_pair(Tag.OrderID, order_id.encode())
    msg.append_pair(Tag.ClOrdID, cl_ord_id.encode())
    msg.append_pair(Tag.OrigClOrdID, orig_cl_ord_id.encode())
    msg.append_pair(Tag.OrdStatus, ord_status)
    msg.append_pair(Tag.TransactTime, _utc_now())
    msg.append_pair(Tag.Text, text.encode())
    return msg
