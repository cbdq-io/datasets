Feature: Test Data Package Files Against the Relevant JSON Schema

  Scenario Outline: Data Packages
    Given the JSON Schema URL of <json_schema_url>
    And the Data Package File of <data_package_file_name>
    When the Data Package File Exists
    Then the Data Package File Validates Against the Schema

    Examples:
        | json_schema_url                                                     | data_package_file_name                                  |
        | https://specs.frictionlessdata.io/schemas/tabular-data-package.json | uk/gov/metoffice/historic_station_data/datapackage.json |
        | https://specs.frictionlessdata.io/schemas/tabular-data-package.json | uk/gov/exchange_rates/datapackage.json                  |
