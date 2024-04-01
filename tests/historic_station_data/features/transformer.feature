Feature: Transformer
  Ensure that we can parse any combination of the data that is provided by
  the Met Office Historic Station data.

  Scenario Outline: Parse Record by Line Number
    Given the Sample Input Data
    And the station name is <station_name>
    When the line number is <line_number>
    Then the record <attribute> is set to <value>

    Examples:
        | station_name | line_number | attribute        | value    |
        | camborne     | 1           | metadata         | Camborne |
        | camborne     | 1           | month            | Empty    |
        | camborne     | 8           | month            | 1978-09  |
        | camborne     | 8           | sun_is_estimated | None     |


  Scenario Outline: Parse Record by Month
    Given the Sample Input Data
    And the station name is <station_name>
    When the month is <month>
    Then the record <attribute> is set to <value>

    Examples:
        | station_name | month   | attribute         | value                    |
        | camborne     | 1978-09 | station_name      | camborne                 |
        | camborne     | 1978-09 | metadata          | Empty                    |
        | camborne     | 1978-09 | month             | 1978-09                  |
        | camborne     | 1978-09 | tmax              | 17.5                     |
        | camborne     | 1978-09 | tmax_is_estimated | False                    |
        | camborne     | 1978-09 | tmin              | 11.3                     |
        | camborne     | 1978-09 | tmin_is_estimated | False                    |
        | camborne     | 1978-09 | af                | 0                        |
        | camborne     | 1978-09 | af_is_estimated   | False                    |
        | camborne     | 1978-09 | rain              | 26.7                     |
        | camborne     | 1978-09 | rain_is_estimated | False                    |
        | camborne     | 1978-09 | sun               | None                     |
        | camborne     | 1978-09 | sun_is_estimated  | None                     |
        | camborne     | 1978-09 | sun_instrument    | None                     |
        | camborne     | 1978-09 | provisional       | False                    |
        | camborne     | 1979-03 | sun               | 105.0                    |
        | camborne     | 1979-03 | sun_is_estimated  | False                    |
        | camborne     | 1979-03 | sun_instrument    | Campbell Stokes recorder |
        | camborne     | 2007-07 | sun               | 190.3                    |
        | camborne     | 2007-07 | sun_is_estimated  | False                    |
        | camborne     | 2007-07 | sun_instrument    | Kipp & Zonen sensor      |
        | camborne     | 2023-07 | sun               | 137.6                    |
        | camborne     | 2023-07 | sun_is_estimated  | True                     |
        | camborne     | 2023-07 | sun_instrument    | None                     |
        | camborne     | 2023-07 | provisional       | True                     |
        | lowestoft    | 1945-03 | rain              | 35.8                     |
        | lowestoft    | 1945-03 | sun               | None                     |
        | lowestoft    | 1945-03 | sun_is_estimated  | None                     |
        | lowestoft    | 2007-09 | sun               | 152.0                    |
        | lowestoft    | 2007-09 | sun_is_estimated  | False                    |
        | lowestoft    | 2007-09 | sun_instrument    | Campbell Stokes recorder |
        | lowestoft    | 2009-10 | sun               | 81.6                     |
        | lowestoft    | 2009-10 | sun_is_estimated  | True                     |
        | lowestoft    | 2009-10 | sun_instrument    | None                     |
        | whitby       | 1976-01 | sun               | 57.1                     |
        | whitby       | 1976-01 | sun_instrument    | Campbell Stokes recorder |
        | whitby       | 1976-01 | sun_is_estimated  | False                    |
        | whitby       | 2000-01 | sun               | 71.6                     |
        | whitby       | 2000-01 | sun_instrument    | Campbell Stokes recorder |
        | whitby       | 2000-01 | sun_is_estimated  | False                    |
