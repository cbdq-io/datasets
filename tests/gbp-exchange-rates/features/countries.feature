Feature: Validate the Country Names
    In order to validate the country names
    As a data wrangler
    I want to ensure that the country names are recognised

Scenario: Cross Reference the Country Names Against our Country Data
    Given the list of currency countries
    And the list of country data countries
    When the lists are captured
    Then ensure the country name is in the country data
