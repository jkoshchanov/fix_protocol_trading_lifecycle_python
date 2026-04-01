Feature: Order Cancel Request (35=F) and Cancel Reject (35=9)
  As a trader
  I want to cancel open orders using FIX protocol
  So that I can manage my positions and risk

  Scenario: Trader sends a cancel request for an open order
    Given a cancel request for original order "ORD-001" with new clordid "CXLORD-001"
    When the cancel request is built
    Then the message type should be OrderCancelRequest
    And the OrigClOrdID should be "ORD-001"
    And the ClOrdID should be "CXLORD-001"
    And the symbol should be "AAPL"

  Scenario: Broker rejects a cancel request for an already filled order
    Given a cancel reject for order "CXLORD-002" referencing "ORD-999"
    When the cancel reject is received
    Then the message type should be OrderCancelReject
    And the cancel reject should contain a rejection reason
    And the order status should be Filled
