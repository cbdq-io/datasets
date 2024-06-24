#!/usr/bin/env python
"""
A script for running Great Expectations.

Copyright (C) 2024 Cloud Based DQ Ltd. This program is free software: you can
redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. This program is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
the GNU General Public License for more details. You should have received a
copy of the GNU General Public License along with this program. If not,
see <http://www.gnu.org/licenses/>.
"""
import argparse
import csv
import logging
from pathlib import Path

import great_expectations as gx
import pandas as pd

HISTORIC_STATION_DATA_PATH = 'uk/gov/metoffice/historic_station_data/data/historic-station-data.csv'
PROG = Path(__file__).stem
logging.basicConfig()
logger = logging.getLogger(PROG)


class Extractor:
    """
    Extract data from the CSV created by the ETL script.

    Attributes
    ----------
    data_path : str
        The path to the data to be extracted from.

    Parameters
    ----------
    data_path : str
        The path to the data to be extracted from.
    """

    def __init__(self, data_path: str) -> None:
        """Create an Extractor class."""
        self.data_path = data_path

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get a pandas dataframe without any of the metadata.

        Returns
        -------
        pd.DataFrame
            The non-metadata dataframe of the dataset.
        """
        with open(self.data_path) as stream:
            reader = self.reader(stream)
            df = pd.DataFrame(reader)

        return df

    def reader(self, stream) -> None:
        """
        Read CSV data from input file and yield rows as dictionaries.

        Parameters
        ----------
        stream :
            An input stream to read the CSV data from.

        Yields
        ------
        dict
            An individual row of data.
        """
        reader = csv.DictReader(stream)

        for row in reader:
            if row['metadata']:
                continue

            del row['metadata']

            for key, value in row.items():
                if value == '':
                    row[key] = None

            yield row


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="""
        Extract, transform and load UK Met Office historical station data.
        """
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--debug', action='store_true', help='Set debug log level.')
    group.add_argument('-v', '--verbose', action='store_true', help='Set info log level.')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logger.setLevel(logging.INFO)

    extractor = Extractor(HISTORIC_STATION_DATA_PATH)
    all_data = extractor.get_dataframe()
    logger.info(f'Loaded {len(all_data):,} rows from "{HISTORIC_STATION_DATA_PATH}".')
    latest_month = all_data.loc[all_data['month'].idxmax()]['month']
    logger.info(f'The latest month in the dataset is "{latest_month}".')
    station_names = sorted(all_data['station_name'].unique())
    context = gx.get_context()
    suite = context.get_expectation_suite(expectation_suite_name='metoffice_historical_station_data')
    datasource = context.sources.add_or_update_pandas('metoffice_historical_station_data')
    asset_name = 'metoffice-historical-station-data'
    asset = datasource.add_dataframe_asset(asset_name, all_data)
    batch_request = asset.build_batch_request()
    checkpoint = context.add_or_update_checkpoint(
        name=f'{asset_name}-{latest_month}',
        validations=[
            {
                'batch_request': batch_request,
                'expectation_suite_name': 'metoffice_historical_station_data'
            }
        ]
    )
    check_point_result = checkpoint.run(run_name=latest_month)
