#!/usr/bin/env python
"""
National Statistics Postcode Lookup.

Extract CSV data from the Zip Archive downloaded from
<https://geoportal.statistics.gov.uk/datasets/8a1d5b58df824b2e86fe07ddfdd87165/about>.
"""
import argparse
import logging
import os
import sys
import zipfile

from pathlib import Path

PROG = os.path.basename(sys.argv[0])
logging.basicConfig()
logger = logging.getLogger(PROG)


def main(input: str, output: str) -> None:
    """Extract the data from the archive and write to a data directory."""
    logger.debug(f'Creating "{output}"...')
    p = Path(output)
    p.mkdir()

    with zipfile.ZipFile(input, 'r') as zip:
        for input_name in zip.namelist():
            if input_name.startswith('Data/multi_csv/'):
                continue

            if not input_name.endswith('.csv'):
                continue

            output_name = input_name \
                .replace(' ', '_') \
                .replace('(', '') \
                .replace(')', '')
            output_name = f'{output}/{output_name}'
            logger.debug(f'Extracting "{input_name}" to "{output_name}"...')
            dirname = os.path.dirname(output_name)
            p = Path(dirname)
            p.mkdir(parents=True, exist_ok=True)

            with open(output_name, 'wb') as stream:
                stream.write(zip.read(input_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=PROG)
    parser.add_argument(
        '-d', '--debug',
        help='Enable debug level logging.',
        action='store_true',
        required=False
    )
    parser.add_argument(
        '-i', '--input',
        help='The path to the downloaded Zip archive',
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        help='The path to the [not yet existing] directory to load the data.',
        required=True
    )
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Log level is DEBUG')
    else:
        logger.setLevel(logging.INFO)

    main(args.input, args.output)
