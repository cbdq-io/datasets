"""Extract Parser feature tests."""
import json
import os

from extract import ExtractMapper
from pytest_bdd import given, parsers, scenario, then, when

bdd_features_base_dir = f'{os.path.dirname(os.path.realpath(__file__))}/../features'
line = None


@scenario(f'{bdd_features_base_dir}/extract-parser.feature', 'Parse Record by Line Number')
def test_parse_record_by_line_number():
    """Parse Record by Line Number."""


@scenario(f'{bdd_features_base_dir}/extract-parser.feature', 'Parse Record by Month')
def test_parse_record_by_month():
    """Parse Record by Month."""


@given('the Sample Input Data', target_fixture='sample_data')
def _():
    """the Sample Input Data."""
    with open(f'{bdd_features_base_dir}/../resources/sample-data.json') as stream:
        data = json.load(stream)

    return data


@given(parsers.parse('the station name is {station_name}'), target_fixture='station_name')
def _(station_name: str):
    """the station name is <station_name>."""
    return station_name


@when(parsers.parse('the line number is {line_number}'))
def _(line_number: str, sample_data, station_name):
    """the line number is <line_number>."""
    global line
    line = sample_data['stations'][station_name]['lines'][line_number]


@when(parsers.parse('the month is {month}'))
def _(month: str, sample_data, station_name):
    """the month is <month>."""
    global line
    line = sample_data['stations'][station_name]['months'][month]


@then(parsers.parse('the record {attribute} is set to {expected_value}'))
def _(attribute: str, expected_value: str, station_name):
    """the record <attribute> is set to <value>."""
    global line
    expected_value_map = {
        'None': None,
        'True': True,
        'False': False
    }

    attribute_type_map = {
        'station_name': str,
        'metadata': str,
        'month': str,
        'tmax': float,
        'tmin': float,
        'af': int,
        'rain': float,
        'sun': float,
        'sun_instrument': str
    }

    if expected_value in expected_value_map:
        expected_value = expected_value_map[expected_value]

    if type(expected_value) is str:
        expected_value = attribute_type_map[attribute](expected_value)

    extract_mapper = ExtractMapper(station_name, line)
    data = extract_mapper.to_dict()
    actual_value = data[attribute]
    message = f'Expected {expected_value}: {type(expected_value)} but got {actual_value}: {type(actual_value)}.'
    assert actual_value == expected_value, f'{message} "{line}".'
