#!/usr/bin/env python
"""A Flyte Kit workflow to ETL the GBP exchange rate."""
import calendar
import csv
import datetime
import json
import os
from datetime import date, timedelta

import logger
import pandas as pd
import smart_open
from flytekit import task, workflow


class ExchangeRate:
    """
    A class for handling exchange rate data.

    Parameters
    ----------
    load_file_name : str, optional
        The name of the file to load the data to, by default 'uk/gov/exchange_rates/data/gbp-exchange-rate.csv'
    """

    def __init__(self, load_file_name: str = 'uk/gov/exchange_rates/data/gbp-exchange-rate.csv') -> None:
        """Create an ExchangeRate object."""
        self._actual_month = None
        self._expected_month = None
        self.load_file_name = load_file_name
        self._today = date.today()

    def actual_month(self) -> str:
        """
        Get the last month that we loaded.

        Returns
        -------
        str
            The last month we loaded as an ISO 8601 string.
        """
        response = None

        with open(self.load_file_name, 'rt') as stream:
            reader = csv.DictReader(stream)

            for record in reader:
                month = record['month']

                if response is None or month > response:
                    response = month

        self._actual_month = response
        return response

    def expected_month(self) -> str:
        """
        Calculate what month the data is available for.

        HMRC publish rates for the following month are published on the
        penultimate Thursday of every month.

        Returns
        -------
        str
            An ISO 8601 date (yyyy-mm) of the expected date.
        """
        today = self.today()
        year = today.year
        month = today.month
        last_day_of_month = calendar.monthrange(year, month)[1]
        last_date = date(year, month, last_day_of_month)
        last_thursday = last_date - timedelta(days=(last_date.weekday() - 3) % 7)
        penultimate_thursday = last_thursday - timedelta(days=7)

        if today < penultimate_thursday:
            response = today
        else:
            response = last_date + timedelta(days=1)

        response = response.strftime('%Y-%m')
        self._expected_month = response
        return response

    def extract_generator(self) -> None:
        """Create a generator for extracting the data."""
        with open(self.load_file_name, 'rt') as stream:
            reader = csv.DictReader(stream)

            for record in reader:
                yield record

        months = self.missing_months()

        for iso_month in months:
            month = datetime.datetime.strptime(iso_month, '%Y-%m')
            url = 'https://www.trade-tariff.service.gov.uk/api/v2/exchange_rates/files/monthly_csv_'
            url += f'{month.year}-{month.month}.csv'

            with smart_open.open(url, 'rt') as stream:
                reader = csv.DictReader(stream)

                for input_record in reader:
                    output_record = {
                        'month': iso_month,
                        'country_or_territory': input_record['Country/Territories'],
                        'currency': input_record['Currency'],
                        'code': input_record['Currency Code'],
                        'rate': input_record['Currency Units per £1']
                    }
                    yield output_record

    def missing_months(self) -> list:
        """
        Get a list of missing URLs.

        Returns
        -------
        list
            A list of missing months in ISO 8601 format.
        """
        start_date = datetime.datetime.strptime(self._actual_month, '%Y-%m')
        end_date = datetime.datetime.strptime(self._expected_month, '%Y-%m')
        month_list = []
        year = start_date.year
        month = start_date.month

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        iso_date = f'{year:04d}-{month:02d}-01'
        current_date = datetime.datetime.fromisoformat(iso_date)

        while current_date <= end_date:
            month_list.append(current_date.strftime('%Y-%m'))
            # Increment by one month
            next_month = current_date.month % 12 + 1
            next_year = current_date.year + (current_date.month // 12)
            current_date = current_date.replace(year=next_year, month=next_month)

        return month_list

    def today(self, today: date = None) -> date:
        """
        Get or set the date used as an offset.

        Parameters
        ----------
        today : date, optional
            The date to set the object value to, by default None

        Returns
        -------
        date
            The date value as set in the object.
        """
        if today is not None:
            self._today = today

        return self._today


PROG = os.path.basename(__file__).removesuffix('.py')
logger = logger.get_logger(PROG)
exchange_rate = ExchangeRate()
actual_month = exchange_rate.actual_month()
logger.info(f'Actual month is "{actual_month}".')
expected_month = exchange_rate.expected_month()
logger.info(f'Expected month is "{expected_month}".')


@task()
def extract() -> pd.DataFrame:
    """
    Extract data from the HMRC site and append to the existing loaded data.

    Returns
    -------
    pd.DataFrame
        A Pandas dataframe containing the extracted data.
    """
    reader = exchange_rate.extract_generator()
    return pd.DataFrame(reader)


@task()
def load(df: pd.DataFrame) -> None:
    """
    Load the data to CSV and update the datapackage.json file.

    Parameters
    ----------
    df : pd.DataFrame
        The data to be loaded into the CSV file.
    """
    df.to_csv(exchange_rate.load_file_name, index=False)

    with open('uk/gov/exchange_rates/datapackage.json', 'rt') as stream:
        data_package = json.load(stream)

    data_package['version'] = os.getenv('GIT_TAG')
    now = datetime.datetime.now(datetime.UTC)
    data_package['created'] = now.isoformat(timespec='seconds')

    with open('uk/gov/exchange_rates/datapackage.json', 'wt') as stream:
        json.dump(data_package, stream, indent=4, sort_keys=True)


@workflow
def wf():
    """Execute the workflow."""
    df = extract()
    load(df=df)


if __name__ == '__main__':
    # Execute the workflow by invoking it like a function and passing in
    # the necessary parameters
    if actual_month != expected_month:
        wf()
    else:
        logger.info('No new data available.')
