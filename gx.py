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
import os
from pathlib import Path

import great_expectations as gx
import pandas as pd
from great_expectations.render.renderer import (ExpectationSuitePageRenderer,
                                                ValidationResultsPageRenderer)
from great_expectations.render.view import DefaultMarkdownPageView

HISTORIC_STATION_DATA_PATH = 'uk/gov/metoffice/historic_station_data/data/historic-station-data.csv'
PROG = Path(__file__).stem
logging.basicConfig()
logger = logging.getLogger(PROG)


def generate_markdown_reports(context: gx.data_context.data_context.file_data_context.FileDataContext,
                              checkpoint_result: gx.checkpoint.types.checkpoint_result.CheckpointResult,
                              output_dir: str) -> None:
    """
    Generate Markdown reports from the expectation suites and validation results.

    Parameters
    ----------
    context : great_expectations.data_context.data_context.file_data_context.FileDataContext
        The data context.
    checkpoint_result : great_expectations.checkpoint.types.checkpoint_result.CheckpointResult
        The result of the checkpoint just executed.
    output_dir : str
        The path to the directory to write the reports to.
    """
    # Generate markdown for all expectation suites
    for suite_name in context.list_expectation_suite_names():
        suite = context.get_expectation_suite(suite_name)
        suite_renderer = ExpectationSuitePageRenderer().render(suite)
        suite_md = DefaultMarkdownPageView().render(suite_renderer)
        suite_md_path = os.path.join(output_dir, f'{suite_name}_expectations.md')

        with open(suite_md_path, 'w') as stream:
            stream.write(suite_md)

    # Generate markdown for all validation results
    for validation_result_identifier in checkpoint_result.list_validation_result_identifiers():
        run_id = validation_result_identifier.run_id
        validation_result = context.get_validation_result(suite_name, run_id)
        validation_renderer = ValidationResultsPageRenderer().render(validation_result)
        validation_md = DefaultMarkdownPageView().render(validation_renderer)
        file_name = f'{run_id.run_name}_{suite_name}_validation.md'
        validation_md_path = os.path.join(output_dir, file_name)
        logger.info(f'Writing validation to "{validation_md_path}".')

        with open(validation_md_path, 'w') as stream:
            stream.write(validation_md)


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
    asset_name = 'ALL'
    asset = datasource.add_dataframe_asset('ALL', all_data)
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
    output_dir = 'docs/markdown_reports'
    generate_markdown_reports(context, check_point_result, output_dir)
