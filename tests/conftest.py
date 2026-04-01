import pytest
from pytest_bdd import given, when, then, parsers
from fix_messages.constants import Side, OrdType, OrdStatus, ExecType, Tag
from fix_messages.message_builder import (
    build_new_order_single,
    build_execution_report,
    build_order_cancel_request,
    build_order_cancel_replace_request,
    build_order_cancel_reject,
)
from validators.fix_validator import (
    assert_field_equals,
    assert_numeric_equals,
    assert_field_present,
    validate_fill_quantities,
)


@pytest.fixture
def context():
    """Shared mutable state passed between BDD steps within a scenario."""
    return {}


# ==========================================================================
# Given steps
# ==========================================================================

@given(parsers.parse('a limit buy order for "{symbol}" with quantity {qty:d} and price {price:f}'))
def limit_buy_order(context, symbol, qty, price):
    context["msg"] = build_new_order_single(
        cl_ord_id="ORD-001",
        symbol=symbol,
        side=Side.Buy,
        order_qty=qty,
        ord_type=OrdType.Limit,
        price=price,
    )


@given(parsers.parse('a market sell order for "{symbol}" with quantity {qty:d}'))
def market_sell_order(context, symbol, qty):
    context["msg"] = build_new_order_single(
        cl_ord_id="ORD-002",
        symbol=symbol,
        side=Side.Sell,
        order_qty=qty,
        ord_type=OrdType.Market,
    )


@given(parsers.parse('an execution report for order "{cl_ord_id}" with status New'))
def exec_report_new(context, cl_ord_id):
    context["msg"] = build_execution_report(
        order_id="BRKR-001",
        cl_ord_id=cl_ord_id,
        exec_id="EXEC-001",
        exec_type=ExecType.New,
        ord_status=OrdStatus.New,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=100,
        cum_qty=0,
        avg_px=0.0,
    )


@given(parsers.parse('an execution report for order "{cl_ord_id}" with status PartiallyFilled'))
def exec_report_partial(context, cl_ord_id):
    context["msg"] = build_execution_report(
        order_id="BRKR-001",
        cl_ord_id=cl_ord_id,
        exec_id="EXEC-002",
        exec_type=ExecType.PartialFill,
        ord_status=OrdStatus.PartiallyFilled,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=60,
        cum_qty=40,
        avg_px=149.95,
        last_qty=40,
        last_px=149.95,
    )


@given(parsers.parse('an execution report for order "{cl_ord_id}" with status Filled'))
def exec_report_filled(context, cl_ord_id):
    context["msg"] = build_execution_report(
        order_id="BRKR-001",
        cl_ord_id=cl_ord_id,
        exec_id="EXEC-003",
        exec_type=ExecType.Fill,
        ord_status=OrdStatus.Filled,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=0,
        cum_qty=100,
        avg_px=149.97,
        last_qty=60,
        last_px=150.00,
    )


@given(parsers.parse('an execution report for order "{cl_ord_id}" with status Rejected and text "{text}"'))
def exec_report_rejected(context, cl_ord_id, text):
    context["msg"] = build_execution_report(
        order_id="BRKR-002",
        cl_ord_id=cl_ord_id,
        exec_id="EXEC-010",
        exec_type=ExecType.Rejected,
        ord_status=OrdStatus.Rejected,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=0,
        cum_qty=0,
        avg_px=0.0,
        text=text,
    )


@given(parsers.parse('a cancel request for original order "{orig_cl_ord_id}" with new clordid "{cl_ord_id}"'))
def cancel_request(context, orig_cl_ord_id, cl_ord_id):
    context["msg"] = build_order_cancel_request(
        cl_ord_id=cl_ord_id,
        orig_cl_ord_id=orig_cl_ord_id,
        symbol="AAPL",
        side=Side.Buy,
        order_qty=100,
    )


@given(parsers.parse('a cancel reject for order "{cl_ord_id}" referencing "{orig_cl_ord_id}"'))
def cancel_reject(context, cl_ord_id, orig_cl_ord_id):
    context["msg"] = build_order_cancel_reject(
        order_id="BRKR-001",
        cl_ord_id=cl_ord_id,
        orig_cl_ord_id=orig_cl_ord_id,
        ord_status=OrdStatus.Filled,
        text="Too late to cancel — order already filled",
    )


@given(parsers.parse('a replace request for original order "{orig_cl_ord_id}" with new clordid "{cl_ord_id}"'))
def replace_request_base(context, orig_cl_ord_id, cl_ord_id):
    context["orig_cl_ord_id"] = orig_cl_ord_id
    context["cl_ord_id"] = cl_ord_id


@given(parsers.parse("the new quantity is {qty:d} and the new price is {price:f}"))
def replace_request_with_qty_price(context, qty, price):
    context["msg"] = build_order_cancel_replace_request(
        cl_ord_id=context["cl_ord_id"],
        orig_cl_ord_id=context["orig_cl_ord_id"],
        symbol="AAPL",
        side=Side.Buy,
        order_qty=qty,
        ord_type=OrdType.Limit,
        price=price,
    )


# ==========================================================================
# When steps
# ==========================================================================

@when("the order is built as a NewOrderSingle message")
def order_built(context):
    assert context["msg"] is not None


@when("the execution report is received")
def execution_report_received(context):
    assert context["msg"] is not None


@when("the cancel request is built")
def cancel_request_built(context):
    assert context["msg"] is not None


@when("the cancel reject is received")
def cancel_reject_received(context):
    assert context["msg"] is not None


@when("the replace request is built")
def replace_request_built(context):
    assert context["msg"] is not None


@when("the broker acknowledges the order")
def broker_ack(context):
    context["msg"] = build_execution_report(
        order_id="BRKR-001",
        cl_ord_id="ORD-001",
        exec_id="EXEC-001",
        exec_type=ExecType.New,
        ord_status=OrdStatus.New,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=100,
        cum_qty=0,
        avg_px=0.0,
    )


@when(parsers.parse("the order is partially filled with qty {qty:d} at price {price:f}"))
def partial_fill(context, qty, price):
    context["msg"] = build_execution_report(
        order_id="BRKR-001",
        cl_ord_id="ORD-001",
        exec_id="EXEC-002",
        exec_type=ExecType.PartialFill,
        ord_status=OrdStatus.PartiallyFilled,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=100 - qty,
        cum_qty=qty,
        avg_px=price,
        last_qty=qty,
        last_px=price,
    )


@when(parsers.parse("the order is fully filled with remaining qty {qty:d} at price {price:f}"))
def full_fill(context, qty, price):
    context["msg"] = build_execution_report(
        order_id="BRKR-001",
        cl_ord_id="ORD-001",
        exec_id="EXEC-003",
        exec_type=ExecType.Fill,
        ord_status=OrdStatus.Filled,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=0,
        cum_qty=100,
        avg_px=price,
        last_qty=qty,
        last_px=price,
    )


@when(parsers.parse('the trader sends a cancel request with clordid "{cl_ord_id}"'))
def send_cancel(context, cl_ord_id):
    context["msg"] = build_order_cancel_request(
        cl_ord_id=cl_ord_id,
        orig_cl_ord_id="ORD-001",
        symbol="AAPL",
        side=Side.Buy,
        order_qty=100,
    )


@when("the broker confirms the cancellation")
def broker_confirms_cancel(context):
    context["msg"] = build_execution_report(
        order_id="BRKR-001",
        cl_ord_id="CXLORD-001",
        exec_id="EXEC-004",
        exec_type=ExecType.Cancelled,
        ord_status=OrdStatus.Cancelled,
        symbol="AAPL",
        side=Side.Buy,
        leaves_qty=0,
        cum_qty=0,
        avg_px=0.0,
    )


@when(parsers.parse('the trader sends a replace request with clordid "{cl_ord_id}" new qty {qty:d} and price {price:f}'))
def send_replace(context, cl_ord_id, qty, price):
    context["msg"] = build_order_cancel_replace_request(
        cl_ord_id=cl_ord_id,
        orig_cl_ord_id="ORD-001",
        symbol="AAPL",
        side=Side.Buy,
        order_qty=qty,
        ord_type=OrdType.Limit,
        price=price,
    )


# ==========================================================================
# Then steps
# ==========================================================================

@then("the message type should be NewOrderSingle")
def check_msg_type_new_order(context):
    assert_field_equals(context["msg"], Tag.MsgType, b"D", "MsgType")


@then("the message type should be ExecutionReport")
def check_msg_type_exec_report(context):
    assert_field_equals(context["msg"], Tag.MsgType, b"8", "MsgType")


@then("the message type should be OrderCancelRequest")
def check_msg_type_cancel_request(context):
    assert_field_equals(context["msg"], Tag.MsgType, b"F", "MsgType")


@then("the message type should be OrderCancelReject")
def check_msg_type_cancel_reject(context):
    assert_field_equals(context["msg"], Tag.MsgType, b"9", "MsgType")


@then("the message type should be OrderCancelReplaceRequest")
def check_msg_type_replace(context):
    assert_field_equals(context["msg"], Tag.MsgType, b"G", "MsgType")


@then(parsers.parse('the symbol should be "{symbol}"'))
def check_symbol(context, symbol):
    assert_field_equals(context["msg"], Tag.Symbol, symbol.encode(), "Symbol")


@then("the side should be Buy")
def check_side_buy(context):
    assert_field_equals(context["msg"], Tag.Side, Side.Buy, "Side")


@then("the side should be Sell")
def check_side_sell(context):
    assert_field_equals(context["msg"], Tag.Side, Side.Sell, "Side")


@then(parsers.parse("the order quantity should be {qty:d}"))
def check_order_qty(context, qty):
    assert_numeric_equals(context["msg"], Tag.OrderQty, qty, "OrderQty")


@then(parsers.parse("the price should be {price:f}"))
def check_price(context, price):
    assert_numeric_equals(context["msg"], Tag.Price, price, "Price")


@then("the order type should be Limit")
def check_ord_type_limit(context):
    assert_field_equals(context["msg"], Tag.OrdType, OrdType.Limit, "OrdType")


@then("the order type should be Market")
def check_ord_type_market(context):
    assert_field_equals(context["msg"], Tag.OrdType, OrdType.Market, "OrdType")


@then(parsers.parse('the BeginString should be "{value}"'))
def check_begin_string(context, value):
    assert_field_equals(context["msg"], Tag.BeginString, value.encode(), "BeginString")


@then(parsers.parse('the SenderCompID should be "{value}"'))
def check_sender(context, value):
    assert_field_equals(context["msg"], Tag.SenderCompID, value.encode(), "SenderCompID")


@then(parsers.parse('the TargetCompID should be "{value}"'))
def check_target(context, value):
    assert_field_equals(context["msg"], Tag.TargetCompID, value.encode(), "TargetCompID")


@then("the TransactTime field should be present")
def check_transact_time(context):
    assert_field_present(context["msg"], Tag.TransactTime)


@then("the order status should be New")
def check_status_new(context):
    assert_field_equals(context["msg"], Tag.OrdStatus, OrdStatus.New, "OrdStatus")


@then("the order status should be PartiallyFilled")
def check_status_partial(context):
    assert_field_equals(context["msg"], Tag.OrdStatus, OrdStatus.PartiallyFilled, "OrdStatus")


@then("the order status should be Filled")
def check_status_filled(context):
    assert_field_equals(context["msg"], Tag.OrdStatus, OrdStatus.Filled, "OrdStatus")


@then("the order status should be Rejected")
def check_status_rejected(context):
    assert_field_equals(context["msg"], Tag.OrdStatus, OrdStatus.Rejected, "OrdStatus")


@then("the order status should be Cancelled")
def check_status_cancelled(context):
    assert_field_equals(context["msg"], Tag.OrdStatus, OrdStatus.Cancelled, "OrdStatus")


@then("the execution type should be New")
def check_exec_type_new(context):
    assert_field_equals(context["msg"], Tag.ExecType, ExecType.New, "ExecType")


@then("the execution type should be PartialFill")
def check_exec_type_partial(context):
    assert_field_equals(context["msg"], Tag.ExecType, ExecType.PartialFill, "ExecType")


@then("the execution type should be Fill")
def check_exec_type_fill(context):
    assert_field_equals(context["msg"], Tag.ExecType, ExecType.Fill, "ExecType")


@then(parsers.parse("the LeavesQty should be {qty:d}"))
def check_leaves_qty(context, qty):
    assert_numeric_equals(context["msg"], Tag.LeavesQty, qty, "LeavesQty")


@then(parsers.parse("the CumQty should be {qty:d}"))
def check_cum_qty(context, qty):
    assert_numeric_equals(context["msg"], Tag.CumQty, qty, "CumQty")


@then(parsers.parse("the fill quantities should balance for total order qty {total:d}"))
def check_fill_balance(context, total):
    validate_fill_quantities(context["msg"], total_qty=total)


@then(parsers.parse('the rejection reason should be "{text}"'))
def check_rejection_reason(context, text):
    assert_field_present(context["msg"], Tag.Text)
    assert_field_equals(context["msg"], Tag.Text, text.encode(), "Text")


@then(parsers.parse('the OrigClOrdID should be "{orig_cl_ord_id}"'))
def check_orig_cl_ord_id(context, orig_cl_ord_id):
    assert_field_equals(context["msg"], Tag.OrigClOrdID, orig_cl_ord_id.encode(), "OrigClOrdID")


@then(parsers.parse('the ClOrdID should be "{cl_ord_id}"'))
def check_cl_ord_id(context, cl_ord_id):
    assert_field_equals(context["msg"], Tag.ClOrdID, cl_ord_id.encode(), "ClOrdID")


@then("the cancel reject should contain a rejection reason")
def check_cancel_reject_text(context):
    assert_field_present(context["msg"], Tag.Text)
