"""GBP Exchange Rates feature tests."""
from datetime import date

from pytest_bdd import given, parsers, scenario, then, when

from workflows.gbp_exchange_rates import ExchangeRate


@scenario('../features/gbp_exchange_rates.feature', 'Test that we know what month data will be published')
def test_test_that_we_know_what_month_data_will_be_published():
    """Test that we know what month data will be published."""
    pass


@given('the ExchangeRate object', target_fixture='exchange_rate')
def _():
    """the ExchangeRate object."""
    return ExchangeRate()


@when(parsers.parse('today is {today}'))
def _(today: str, exchange_rate: ExchangeRate) -> None:
    """today is <today>."""
    today = date.fromisoformat(today)
    exchange_rate.today(today)


@then(parsers.parse('the expected month is {expected_month}'))
def _(expected_month: str, exchange_rate: ExchangeRate):
    """the expected month is <expected_month>."""
    assert expected_month == exchange_rate.expected_month()
