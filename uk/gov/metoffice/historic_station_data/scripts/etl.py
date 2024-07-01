#!/usr/bin/env python
"""
A script for an etl process on the UK Met Office Historical Station Data.

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
import datetime
import itertools
import json
import logging
import os
import re
import string
from pathlib import Path

import pandas as pd
import smart_open

BASE_DIRECTORY = os.sep.join(__file__.split(os.sep)[:-2])
PROG = Path(__file__).stem
logging.basicConfig()
logger = logging.getLogger(PROG)


class Extractor:
    """
    Extractor class.

    Attributes
    ----------
    STATION_NAMES : str
        A list of the station names.
    df : pandas.Data
    """

    def __init__(self) -> None:
        self.STATION_NAMES = [
            'aberporth',
            'armagh',
            'ballypatrick',
            'bradford',
            'braemar',
            'camborne',
            'cambridge',
            'cardiff',
            'chivenor',
            'cwmystwyth',
            'dunstaffnage',
            'durham',
            'eastbourne',
            'eskdalemuir',
            'heathrow',
            'hurn',
            'lerwick',
            'leuchars',
            'lowestoft',
            'manston',
            'nairn',
            'newtonrigg',
            'oxford',
            'paisley',
            'ringway',
            'rossonwye',
            'shawbury',
            'sheffield',
            'southampton',
            'stornoway',
            'suttonbonington',
            'tiree',
            'valley',
            'waddington',
            'whitby',
            'wickairport',
            'yeovilton'
        ]
        self.df = pd.DataFrame(self.extractor())

    def extractor(self) -> None:
        """
        Extract data from the data sources.

        Yields
        ------
        dict
            A dictionary containing the source URL, the line number and the
            raw input line.
        """
        total_lines = 0

        for station_name in self.STATION_NAMES:
            url = self.input_url(station_name)
            logger.debug(f'Opening "{url}" for reading.')

            with smart_open.open(url, 'r') as input_stream:
                for idx, input_line in enumerate(input_stream):
                    line_number = idx + 1
                    record = {}
                    record['station_name'] = station_name
                    record['input_line'] = input_line
                    yield record

                logger.info(f'Extracted {line_number:,} lines from "{url}".')
                total_lines += line_number

        logger.info(f'Extracted a total of {total_lines:,} lines.')

    def input_url(self, station_name: str) -> str:
        """
        Get the URL path of the data file for the provided station name.

        Parameters
        ----------
        station_name : str
            The station name to provide the URL for.

        Returns
        -------
        str
            The full URL of the location of the station data.
        """
        return f'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{station_name}data.txt'


class SunInstrument:
    """
    A class to parse and persist the sun instrument for a station.

    When the sun instrument has no reading or is estimated, on a row by row
    basis, it is impossible to know the sun instrument type.  This class
    persists the last known sun instrument allowing us to infer the
    instrument type when data is missing/estimated.
    """

    def __init__(self) -> None:
        self._sun_instrument_type = None
        self._station_name = None

    def parse_sun_instrument_token(self, station_name: str, field: str) -> str:
        """
        Parse the sun instrument token/field.

        Parameters
        ----------
        station_name : str
            The name of the station we are processing a row for.
        field : str
            The raw field (cleaned) containing the sun reading.

        Returns
        -------
        str
            None if the sun instrument is unknown, if it is known, then the
            value will either be "Campbell Stokes recorder" or
            "Kipp & Zonen sensor".
        """
        if station_name != self.station_name():
            self.reset_sun_instrument_type()
            self.station_name(station_name)

        if field == '---' or field.endswith('*'):
            return self.sun_instrument_type()

        if field.endswith('#'):
            return self.sun_instrument_type('Kipp & Zonen sensor')

        return self.sun_instrument_type('Campbell Stokes recorder')

    def reset_sun_instrument_type(self) -> None:
        """Reset the instrument type."""
        self._sun_instrument_type = None

    def station_name(self, station_name: str = None) -> str:
        """
        Get/set the station name.

        Parameters
        ----------
        station_name : str, optional
            The station name, by default None

        Returns
        -------
        str
            The station name.
        """
        if station_name is not None:
            self._station_name = station_name

        return self._station_name

    def sun_instrument_type(self, sun_instrument_type: str = None) -> str:
        """
        Get/set the sun instrument type.

        Parameters
        ----------
        sun_instrument_type : str, optional
            The type of sun instrument.

        Returns
        -------
        str
            The type of sun instrument.
        """
        if sun_instrument_type is not None:
            self._sun_instrument_type = sun_instrument_type

        return self._sun_instrument_type


class Transformer:
    """
    Transform the data extracted from the Met Office.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas data frame containing the extracted data.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self._sun_instrument = SunInstrument()
        df['metadata'] = df.apply(self.get_metadata, axis=1)
        df['month'] = df.apply(self.get_month, axis=1)
        df['tmax'] = df.apply(self.get_token_numeric_value, token_index=2, axis=1)
        df['tmax_is_estimated'] = df.apply(self.get_token_numeric_value_is_estimated, token_index=2, axis=1)
        df['tmin'] = df.apply(self.get_token_numeric_value, token_index=3, axis=1)
        df['tmin_is_estimated'] = df.apply(self.get_token_numeric_value_is_estimated, token_index=3, axis=1)
        df['af'] = df.apply(self.get_token_numeric_value, token_index=4, axis=1)
        df['af_is_estimated'] = df.apply(self.get_token_numeric_value_is_estimated, token_index=4, axis=1)
        df['rain'] = df.apply(self.get_token_numeric_value, token_index=5, axis=1)
        df['rain_is_estimated'] = df.apply(self.get_token_numeric_value_is_estimated, token_index=5, axis=1)
        df['sun'] = df.apply(self.get_token_numeric_value, token_index=6, axis=1)
        df['sun_is_estimated'] = df.apply(self.get_token_numeric_value_is_estimated, token_index=6, axis=1)
        df['sun_instrument'] = df.apply(self.get_sun_instrument, axis=1)
        df['provisional'] = df.apply(self.get_is_provisional, axis=1)
        self.df = df

    def clean_sun_data(self, token: str) -> str:
        """
        Clean up the sun token.

        The sun token is the last on the line.  This token seems to be the
        most prone to getting dirty data.  Examples are:

          - lowestoft 2007-09
          - whitby 1976-01 - 2000-01

        Therefore, we strip all non-valid characters from the token.

        Parameters
        ----------
        token : str
            The token to be cleaned.

        Returns
        -------
        str
            The cleaned token.
        """
        disallowed_characters = string.printable
        allowed_characters = ['.', '*', '#', '-', string.digits]
        allowed_characters = list(itertools.chain.from_iterable(allowed_characters))

        for character in allowed_characters:
            disallowed_characters = disallowed_characters.replace(character, '')

        for character in disallowed_characters:
            token = token.replace(character, '')

        return token

    def is_data_record(self, input_line: str) -> bool:
        """
        Identify if the input line is data record.

        Parameters
        ----------
        input_line : str
            The raw input line as extracted.

        Returns
        -------
        bool
            True if the line is a data record or false if it is a metadata
            line.
        """
        line = input_line.strip()
        return line[0].isdigit()

    def get_input_line_tokens(self, input_line: str) -> list:
        """
        Split an input line into tokens for parsing.

        In March 1945, Lowestoft had no data for sun, but didn't add
        the no data field.  We fix that here.

        Parameters
        ----------
        input_line : str
            The raw input line from the source data.

        Returns
        -------
        list
            A list of strings (tokens) parsed from the input line.
        """
        prog = re.compile('[ \t\n\r]+')
        tokens = prog.split(input_line.strip())

        if len(tokens) == 6:
            tokens.append('---')

        tokens[6] = self.clean_sun_data(tokens[6])

        return tokens

    def get_is_provisional(self, row: pd.Series) -> bool:
        """
        Get if the data record is provisional.

        Parameters
        ----------
        row : pd.Series
            A row from a Pandas data frame that contains a input_line.

        Returns
        -------
        bool
            True or False or None if not a data line.
        """
        input_line = row['input_line']

        if not self.is_data_record(input_line):
            return None

        return self.get_input_line_tokens(input_line)[-1] == 'Provisional'

    def get_metadata(self, row: pd.Series) -> str:
        """
        Get the metadata from an input line.

        Parameters
        ----------
        input_line : str
            The raw input line.

        Returns
        -------
        str
            A string of the line or a blank string if the line is a data
            record.
        """
        input_line = row['input_line']

        if self.is_data_record(input_line):
            return ''

        return input_line.strip()

    def get_month(self, row: pd.Series) -> str:
        """
        Return the ISO 8601 month (YYYY-MM) of a data reading.

        Parameters
        ----------
        row : pd.Series
            The data row.

        Returns
        -------
        str
            The ISO 8601 month of a data reading or an empty string if the
            Row is metadata.
        """
        year = self.get_token_numeric_value(row, 0)
        month = self.get_token_numeric_value(row, 1)

        if year:
            return f'{year}-{month:02d}'
        else:
            return ''

    def get_sun_instrument(self, row: pd.Series) -> str:
        """
        Get the sun instrument type.

        Parameters
        ----------
        row : pd.Series
            A row from a Pandas data frame that contains the input_line.

        Returns
        -------
        str
            The type of sun instrument, or None if value not given.
        """
        input_line = row['input_line']

        if not self.is_data_record(input_line):
            return None

        station_name = row['station_name']
        field = str(self.get_input_line_tokens(input_line)[6])
        return self._sun_instrument.parse_sun_instrument_token(station_name, field)

    def get_token_numeric_value(self, row: pd.Series, token_index: int) -> object:
        """
        Split the input line into tokens and then get the value the specified token is.

        Parameters
        ----------
        row : pd.Series
            The row of the Pandas data frame.
        token_index : int
            The index of the token to be parsed.

        Returns
        -------
        object
            Either an int or float of the token value, or None if no value is set.
        """
        funcs = {
            0: int,
            1: int,
            2: float,
            3: float,
            4: int,
            5: float,
            6: float
        }
        input_line = row['input_line']

        if not self.is_data_record(input_line):
            response = None
        else:
            tokens = self.get_input_line_tokens(input_line)
            field = str(tokens[token_index])

            if field == '---':
                response = None
            else:
                field = field.replace('*', '')
                field = field.replace('#', '')
                response = funcs[token_index](field)

        return response

    def get_token_numeric_value_is_estimated(self, row: pd.Series, token_index: int) -> bool:
        """
        Check if the value is an estimate.

        Parameters
        ----------
        row : pd.Series
            A pandas row with an input_string in it.
        token_index : int
            The index of the specific token.

        Returns
        -------
        bool
            True if the value was estimated.
            False if the value is present and not estimated.
            None if the value is not present.
        """
        input_line = row['input_line']

        if not self.is_data_record(input_line):
            return None

        tokens = self.get_input_line_tokens(input_line)
        field = str(tokens[token_index])

        if field == '---':
            return None

        return field.endswith('*')


class Loader:
    """
    Load the data extracted and transformed from the Met Office.

    Parameters
    ----------
    df : pd.DataFrame
        The data having been transformed.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.load_archives()
        self.load_data()
        self.load_package_data()

    def load_archive(self, station_name: str) -> None:
        """
        Load the archive for an individual station.

        Parameters
        ----------
        station_name : str
            The name of the station.
        """
        archive_file_name = f'{BASE_DIRECTORY}{os.sep}archive{os.sep}{station_name}data.txt'
        logger.debug(f'Archiving data for {station_name} to "{archive_file_name}".')
        archive_df = self.df.loc[self.df['station_name'] == station_name]

        with open(archive_file_name, 'wt') as archive_stream:
            archive_stream.writelines(archive_df['input_line'].tolist())

    def load_archives(self) -> None:
        """Load the archive files for all stations."""
        for station_name in self.df['station_name'].unique():
            self.load_archive(station_name)

    def load_data(self) -> None:
        """Load the data to a CSV file."""
        data_filename = f'{BASE_DIRECTORY}{os.sep}data{os.sep}historic-station-data.csv'
        self.df = self.df.drop('input_line', axis=1)
        self.df['metadata_duplicated'] = self.df.duplicated(subset=['metadata'], keep=False)
        self.df['metadata_duplicated'] = self.df.apply(self.qualify_metadata_duplication, axis=1)
        self.df = self.df.drop(self.df[self.df['metadata_duplicated']].index).drop('metadata_duplicated', axis=1)
        logger.info(f'Loading transformed data to "{data_filename}".')
        self.df.to_csv(data_filename, index=False)

    def load_package_data(self) -> None:
        """Update tha datapackage.json file."""
        data_package_file_name = f'{BASE_DIRECTORY}/datapackage.json'

        with open(data_package_file_name) as stream:
            data_package = json.load(stream)

        data_package['version'] = os.environ['GIT_TAG']
        now = datetime.datetime.now(datetime.UTC)
        data_package['created'] = now.isoformat(timespec='seconds')

        with open(data_package_file_name, 'w') as stream:
            json.dump(data_package, stream, indent=4, sort_keys=True)

    def qualify_metadata_duplication(self, row: pd.Series) -> bool:
        """
        Qualify if the metadata is duplicated or empty.

        Parameters
        ----------
        row : pd.Series
            Row from a Pandas data frame.

        Returns
        -------
        bool
            If the data is duplicated or not (false if blank).
        """
        metadata = row['metadata']
        is_duplicated = row['metadata_duplicated']

        if metadata == '':
            is_duplicated = False

        return is_duplicated


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

    extractor = Extractor()
    transformer = Transformer(extractor.df)
    Loader(transformer.df)
