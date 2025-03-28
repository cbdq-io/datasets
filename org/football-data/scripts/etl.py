#!/usr/bin/env python
"""
Transform data from from https://www.football-data.org/ to CSV.

curl -s -H "X-Auth-Token: $FOOTBALL_DATA_API_KEY" \
    https://api.football-data.org/v4/competitions/PL/matches \
    | ./org/football-data/scripts/etl.py
"""
import csv
import json
import sys


class Competition:
    """Process the data for a competition."""

    def __init__(self, data: dict) -> None:
        self._data = data

    def code(self, code: str = None) -> str:
        """
        Get/set the competition code.

        Parameters
        ----------
        code : str, optional
            The competition code to be set, by default None.

        Returns
        -------
        str
            The set competition code.
        """
        if code is not None:
            self._code = code

        return self._code

    def file_name(self) -> str:
        """Get the file name."""
        return f'org/football-data/data/{self.code()}.csv'

    def fixtures(self) -> list[dict]:
        """Return all fixtures from the current competition."""
        response = []

        for match in self.matches():
            self.code(match['competition']['code'])

            if match['status'] == 'FINISHED':
                continue

            response.append(
                {
                    'utcDate': match['utcDate'],
                    'homeTeam': match['homeTeam']['tla'],
                    'awayTeam': match['awayTeam']['tla'],
                    'score': ''
                }
            )

        return response

    def matches(self) -> dict:
        """Get the matches from the competition data."""
        return self._data['matches']

    def results(self) -> list[dict]:
        """Return all results from the current competition."""
        response = []

        for match in self.matches():
            self.code(match['competition']['code'])

            if match['status'] != 'FINISHED':
                continue

            score = f'{match["score"]["fullTime"]["home"]}-'
            score += f'{match["score"]["fullTime"]["away"]}'
            response.append(
                {
                    'utcDate': match['utcDate'],
                    'homeTeam': match['homeTeam']['tla'],
                    'awayTeam': match['awayTeam']['tla'],
                    'score': score
                }
            )

        return response


if __name__ == '__main__':
    competition = Competition(json.load(sys.stdin))

    matches = competition.results()

    with open(competition.file_name(), 'w', newline='') as stream:
        fieldnames = matches[0].keys()
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matches)
        matches = competition.fixtures()
        writer.writerows(matches)
