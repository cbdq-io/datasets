"""Validate the Country Names feature tests."""
import csv

from pytest_bdd import given, scenario, then, when


@scenario('../features/countries.feature', 'Cross Reference the Country Names Against our Country Data')
def test_cross_reference_the_country_names_against_our_country_data():
    """Cross Reference the Country Names Against our Country Data."""


@given('the list of country data countries', target_fixture='country_data_names')
def _():
    """the list of country data countries."""
    response = []

    with open('uk/gov/exchange_rates/data/countries.csv') as stream:
        reader = csv.DictReader(stream)

        for row in reader:
            name = row['name']

            if name not in response:
                response.append(name)

    return response


@given('the list of currency countries', target_fixture='currency_countries')
def _():
    """the list of currency countries."""
    response = []

    with open('uk/gov/exchange_rates/data/gbp-exchange-rate.csv') as stream:
        reader = csv.DictReader(stream)

        for row in reader:
            name = row['country_or_territory']

            if name not in response:
                response.append(name)

    return response


@when('the lists are captured')
def _():
    """the lists are captured."""
    pass


@then('ensure the country name is in the country data')
def _(country_data_names: list, currency_countries: list):
    """ensure the country name is in the country data."""
    for name in currency_countries:
        assert name in country_data_names, f'{name} is missing from the country data.'
