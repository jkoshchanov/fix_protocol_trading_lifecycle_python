# FIX 4.2 Tag constants
class Tag:
    BeginString      = 8
    BodyLength       = 9
    MsgType          = 35
    SenderCompID     = 49
    TargetCompID     = 56
    MsgSeqNum        = 34
    SendingTime      = 52
    CheckSum         = 10

    # Order identification
    ClOrdID          = 11
    OrderID          = 37
    ExecID           = 17
    OrigClOrdID      = 41

    # Instrument
    Symbol           = 55
    SecurityType     = 167
    Currency         = 15

    # Order details
    Side             = 54
    OrderQty         = 38
    OrdType          = 40
    Price            = 44
    StopPx           = 99
    TimeInForce      = 59
    TransactTime     = 60
    HandlInst        = 21

    # Execution details
    OrdStatus        = 39
    ExecType         = 150
    LeavesQty        = 151
    CumQty           = 14
    AvgPx            = 6
    LastPx           = 31
    LastQty          = 32
    Text             = 58

    # Account
    Account          = 1


class MsgType:
    Heartbeat              = b"0"
    Logon                  = b"A"
    Logout                 = b"5"
    NewOrderSingle         = b"D"
    ExecutionReport        = b"8"
    OrderCancelRequest     = b"F"
    OrderCancelReplaceRequest = b"G"
    OrderStatusRequest     = b"H"
    OrderCancelReject      = b"9"
    Reject                 = b"3"


class OrdType:
    Market     = b"1"
    Limit      = b"2"
    Stop       = b"3"
    StopLimit  = b"4"


class Side:
    Buy        = b"1"
    Sell       = b"2"
    SellShort  = b"5"


class OrdStatus:
    New              = b"0"
    PartiallyFilled  = b"1"
    Filled           = b"2"
    Cancelled        = b"4"
    Replaced         = b"5"
    Rejected         = b"8"
    PendingCancel    = b"6"
    PendingReplace   = b"E"


class ExecType:
    New              = b"0"
    PartialFill      = b"1"
    Fill             = b"2"
    Cancelled        = b"4"
    Replaced         = b"5"
    Rejected         = b"8"
    PendingCancel    = b"6"
    PendingReplace   = b"E"


class TimeInForce:
    Day        = b"0"
    GTC        = b"1"
    IOC        = b"3"
    FOK        = b"4"


class HandlInst:
    AutomatedNoIntervention = b"1"
    AutomatedIntervention   = b"2"
    Manual                  = b"3"
