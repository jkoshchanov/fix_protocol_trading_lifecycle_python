Feature: Order Cancel Replace Request (35=G)
  As a trader
  I want to modify an open order using FIX protocol
  So that I can adjust quantity or price without cancelling and re-submitting

  Scenario: Trader modifies quantity and price on an open limit order
    Given a replace request for original order "ORD-001" with new clordid "RPLORD-001"
    And the new quantity is 200 and the new price is 148.50
    When the replace request is built
    Then the message type should be OrderCancelReplaceRequest
    And the OrigClOrdID should be "ORD-001"
    And the ClOrdID should be "RPLORD-001"
    And the order quantity should be 200
    And the price should be 148.50
