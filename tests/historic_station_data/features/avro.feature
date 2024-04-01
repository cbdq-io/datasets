Feature: Avro
  Scenario Outline: Test CSV Rows and Columns Against an Avro Schema
    Given the CSV file called <csv_file>
    And an Avro Schema at <schema_path>
    When the CSV file is read line by line
    Then it should match the schema

    Examples:
        | csv_file                                                              | schema_path                          |
        | uk/gov/metoffice/historic_station_data/data/historic-station-data.csv | avro/avsc/HistoricalStationData.avsc |
