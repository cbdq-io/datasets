"""
Cleaner for the UK Met Office Historic Station Data.

Notes
-----
https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data
"""
import logging
import os
from pathlib import Path

import pandas as pd
import smart_open
from extract import ExtractMapper
from flytekit import task, workflow
from redmx import RateErrorDuration

STATION_ID_LIST = [
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

logging.basicConfig()
logger = logging.getLogger('etl')
logger.setLevel(level=os.getenv('LOG_LEVEL', 'INFO'))


def extract_generator() -> None:
    """
    Read and collate the data from the UK Met Office.

    Iterate over the list of station IDs, read the data files line by line
    and yield the mapped input line.

    Yields
    ------
    dict
        A mapped dictionary as produced by extract.ExtractMapper.do_dict.
    """
    extraction = RateErrorDuration()

    for station_id in STATION_ID_LIST:
        station_extraction = RateErrorDuration()
        url = f'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{station_id}data.txt'
        logger.debug(f'Opening {url} for ingestion.')

        with smart_open.open(url, 'rt') as input_stream:
            for line in input_stream:
                mapped = ExtractMapper(station_id, line)
                extraction.increment_count()
                station_extraction.increment_count()
                yield mapped.to_dict()

        logger.info(f'Extracted {station_extraction.count():,} lines from {url}.')

    logger.info(f'Extracted a total of {extraction.count():,} lines from {len(STATION_ID_LIST)} files.')


@task
def extract() -> pd.DataFrame:
    """Extract the data set."""
    return pd.DataFrame(extract_generator())


@task
def load(data: pd.DataFrame) -> None:
    """Load the data."""
    base_path = f'{os.path.dirname(os.path.realpath(__file__))}'
    metadata = data[data['month'].isnull()] \
        .drop_duplicates(subset=['metadata'], keep=False)[['station_name', 'metadata']]
    data = data[data['metadata'].isnull()].drop('metadata', axis=1)
    data_directory = f'{base_path}/../data'
    Path(data_directory).mkdir(parents=True, exist_ok=True)
    metadata.to_csv(f'{data_directory}/station-metadata.csv', index=False)
    data.to_csv(f'{data_directory}/station-data.csv', index=False)


@workflow
def extract_load() -> None:
    """Work flow to extract and load."""
    data = extract()
    load(data=data)
