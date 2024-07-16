Feature:  GBP Exchange Rates
  Scenario Outline: Test that we know what month data will be published
    Given the ExchangeRate object
    When today is <today>
    Then the expected month is <expected_month>

  Examples:
    | today      | expected_month |
    | 2024-07-15 | 2024-07        |
    | 2024-07-18 | 2024-08        |
