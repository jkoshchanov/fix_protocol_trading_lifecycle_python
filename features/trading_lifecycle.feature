Feature: Full Trading Order Lifecycle
  As a trader
  I want to validate the complete order lifecycle over FIX protocol
  So that I can confirm each stage from order placement to completion

  Scenario: Complete lifecycle — place, acknowledge, partial fill, full fill
    Given a limit buy order for "AAPL" with quantity 100 and price 150.00
    When the order is built as a NewOrderSingle message
    Then the message type should be NewOrderSingle

    When the broker acknowledges the order
    Then the order status should be New
    And the LeavesQty should be 100
    And the CumQty should be 0

    When the order is partially filled with qty 40 at price 149.95
    Then the order status should be PartiallyFilled
    And the CumQty should be 40
    And the LeavesQty should be 60
    And the average price should be 149.95

    When the order is fully filled with remaining qty 60 at price 150.00
    Then the order status should be Filled
    And the CumQty should be 100
    And the LeavesQty should be 0
    And the average price should be 149.98

  Scenario: Place order then cancel before fill
    Given a limit buy order for "AAPL" with quantity 100 and price 150.00
    When the order is built as a NewOrderSingle message
    Then the message type should be NewOrderSingle

    When the trader sends a cancel request with clordid "CXLORD-001"
    Then the message type should be OrderCancelRequest
    And the OrigClOrdID should be "ORD-001"

    When the broker confirms the cancellation
    Then the order status should be Cancelled
    And the LeavesQty should be 0

  Scenario: Place order then modify price before fill
    Given a limit buy order for "AAPL" with quantity 100 and price 150.00
    When the order is built as a NewOrderSingle message
    Then the message type should be NewOrderSingle

    When the trader sends a replace request with clordid "RPLORD-001" new qty 200 and price 148.50
    Then the message type should be OrderCancelReplaceRequest
    And the order quantity should be 200
    And the price should be 148.50
