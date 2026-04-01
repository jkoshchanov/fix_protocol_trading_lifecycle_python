Feature: Execution Report (35=8)
  As a trader
  I want to receive execution reports from the broker
  So that I can track the status of my orders through their lifecycle

  Scenario: Broker acknowledges a new order
    Given an execution report for order "ORD-001" with status New
    When the execution report is received
    Then the message type should be ExecutionReport
    And the order status should be New
    And the execution type should be New
    And the LeavesQty should be 100
    And the CumQty should be 0

  Scenario: Order is partially filled
    Given an execution report for order "ORD-001" with status PartiallyFilled
    When the execution report is received
    Then the message type should be ExecutionReport
    And the order status should be PartiallyFilled
    And the execution type should be PartialFill
    And the CumQty should be 40
    And the LeavesQty should be 60
    And the fill quantities should balance for total order qty 100

  Scenario: Order is fully filled
    Given an execution report for order "ORD-001" with status Filled
    When the execution report is received
    Then the message type should be ExecutionReport
    And the order status should be Filled
    And the execution type should be Fill
    And the CumQty should be 100
    And the LeavesQty should be 0
    And the fill quantities should balance for total order qty 100

  Scenario: Order is rejected by broker
    Given an execution report for order "ORD-005" with status Rejected and text "Risk limit exceeded"
    When the execution report is received
    Then the message type should be ExecutionReport
    And the order status should be Rejected
    And the rejection reason should be "Risk limit exceeded"
