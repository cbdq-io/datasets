"""Avro feature tests."""
import csv
import json

from fastavro import parse_schema
from fastavro.validation import validate_many
from pytest_bdd import given, parsers, scenario, then, when


@scenario('../features/avro.feature', 'Test CSV Rows and Columns Against an Avro Schema')
def test_test_csv_rows_and_columns_against_an_avro_schema():
    """Test CSV Rows and Columns Against an Avro Schema."""


@given(parsers.parse('an Avro Schema at {schema_path}'), target_fixture='schema')
def _(schema_path: str):
    """an Avro Schema at <schema_path>."""
    with open(schema_path, 'r') as stream:
        schema = json.load(stream)

    return parse_schema(schema)


@given(parsers.parse('the CSV file called {csv_file_name}'), target_fixture='csv_reader')
def _(csv_file_name: str):
    """the CSV file called <csv_file>."""
    stream = open(csv_file_name, 'r')
    reader = csv.DictReader(stream)
    return reader


@when('the CSV file is read line by line')
def _():
    """the CSV file is read line by line."""
    pass


@then('it should match the schema')
def _(csv_reader, schema):
    """it should match the schema."""
    assert validate_many(csv_reader, schema, strict=True)
