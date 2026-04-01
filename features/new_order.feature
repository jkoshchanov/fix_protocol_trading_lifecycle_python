Feature: New Order Single (35=D)
  As a trader
  I want to submit a new order using FIX protocol
  So that the broker receives a valid and well-formed order message

  Scenario: Submit a limit buy order for AAPL
    Given a limit buy order for "AAPL" with quantity 100 and price 150.00
    When the order is built as a NewOrderSingle message
    Then the message type should be NewOrderSingle
    And the symbol should be "AAPL"
    And the side should be Buy
    And the order quantity should be 100
    And the price should be 150.00
    And the order type should be Limit

  Scenario: Submit a market sell order for TSLA
    Given a market sell order for "TSLA" with quantity 50
    When the order is built as a NewOrderSingle message
    Then the message type should be NewOrderSingle
    And the symbol should be "TSLA"
    And the side should be Sell
    And the order type should be Market

  Scenario: NewOrderSingle must contain mandatory FIX session fields
    Given a limit buy order for "AAPL" with quantity 100 and price 150.00
    When the order is built as a NewOrderSingle message
    Then the BeginString should be "FIX.4.2"
    And the SenderCompID should be "CLIENT"
    And the TargetCompID should be "BROKER"
    And the TransactTime field should be present
