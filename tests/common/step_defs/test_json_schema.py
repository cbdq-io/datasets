"""Test Data Package Files Against the Relevant JSON Schema feature tests."""

import json
import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pytest_bdd import given, parsers, scenario, then, when
from smart_open import open


@scenario('../features/json-schema.feature', 'Data Packages')
def test_data_packages():
    """Data Packages."""


@given(parsers.parse('the Data Package File of {data_package_file_name}'), target_fixture='data_package')
def _(data_package_file_name: str) -> dict:
    """the Data Package File of <data_package_file_name>."""
    try:
        with open(data_package_file_name) as stream:
            data_package = json.load(stream)
    except FileNotFoundError:
        logging.error(f'File not found "{data_package_file_name}".')
        return None

    return data_package


@given(parsers.parse('the JSON Schema URL of {json_schema_url}'), target_fixture='json_schema')
def _(json_schema_url: str) -> dict:
    """the JSON Schema URL of <json_schema_url>."""
    with open(json_schema_url) as stream:
        json_schema = json.load(stream)

    return json_schema


@when('the Data Package File Exists')
def _(data_package: dict) -> None:
    """the Data Package File Exists."""
    assert data_package is not None, 'Data package not available, see error message.'


@then('the Data Package File Validates Against the Schema')
def _(data_package: dict, json_schema: dict) -> None:
    """the Data Package File Validates Against the Schema."""
    is_valid = False

    try:
        validate(instance=data_package, schema=json_schema)
        is_valid = True
    except ValidationError as ex:
        message = ex.message

    assert is_valid, message
