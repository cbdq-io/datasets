"""
Extract module for the UK Met Office Historic Station Data.

Notes
-----
https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data
"""
import itertools
import re
import string


class ExtractMapper:
    """
    Map the extracted lines from the input file.

    Attributes
    ----------
    station_name : str
        The name of the station that the data is relevant to (e.g. camborne).
    line : str
        The original line extracted from the input file.
    metadata : str
        If the line was metadata, it will be set here.  Otherwise the value
        will be None.
    month : str
        An ISO 8601 date (e.g. 1978-09) of the month the data was recorded.
        If the line was for metadata, this will be None.
    tmax : float
        The maximum temperature recorded during the month.
        Will be None if the input line was metadata or data was not available.
    tmax_is_estimated : bool
        Is the data for tmax estimated or not.
        Will be None if the input line was metadata or data was not available.
    tmin : float
        The minimum temperation recorded during the month.
        Will be None if the input line was metadata or data was not available.
    tmin_is_estimated : bool
        Is the data for tmin estimated or not.
        Will be None if the input line was metadata or data was not available.
    af : int
        Days of air frost recorded.
        Will be None if the input line was metadata or data was not available.
    af_is_estimated : bool
        Is the data for af estimated or not.
        Will be None if the input line was metadata or data was not available.
    rain : float
        The amount of rain in mm recorded during the month.
        Will be None if the input line was metadata or data was not available.
    rain_is_estimated : bool
        Is the data for rain estimated  or not.
        Will be None if the input line was metadata or data was not available.
    sun : float
        The number of hours of sunshine recorded during the month.
        Will be None if the input line was metadata or data was not available.
    sun_is_estimated : bool
        Is the data for sun estimated or not.
        Will be None if the input line was metadata or data was not available.
    sun_instrument : string
        The type of sun instrument used to record sunshine hours.
        Will be None if the input line was metadata or data was not available.
    provisional : bool
        Is the data provisional or not.

    Parameters
    ----------
    station_name : str
        The name of the station that the data was recorded for.
    line | str
        The input line from the data file for the station.
    """

    def __init__(self, station_name: str, line: str) -> None:
        """Create an ExtractMapper object."""
        self.station_name = station_name
        self.line = line
        self.initialise_metadata()
        self.initialise_monthly_data()
        self.parse_line()

    def clean_sun_field(self, field: str) -> str:
        """
        Clean the sun field.

        The sun field is the last field on the input line.  Over the years,
        there has been examples of free text being added to the end of the
        line.  Examples of this are:

          - lowestoft 2007-09
          - whitby 1976-01 - 2000-01.

        These are changes are non-standard and don't follow the expected rules
        of the input.  This method removes all non-standard characters from
        the sun field and return a cleaned up version of it.  Allowed
        characters are:

        - Digits (e.g. 0, 1, 2, 3, 4, 5, 6, 7, 9).
        - Fullstop (.) to indicate floating point accuracy (e.g. "4.2").
        - Asterix (*) indicating that the field value is an estimate.
        - Hash (#) to indicate that the instrument is a Kipp & Zonen sensor.

        Parameters
        ----------
        field : str
            The input field.

        Returns
        -------
        str
            The input field with all non-standard characters removed.
        """
        disallowed_chararcters = string.printable
        allowed_characters = ['.', '*', '#', string.digits]
        allowed_characters = list(itertools.chain.from_iterable(allowed_characters))

        for character in allowed_characters:
            disallowed_chararcters = disallowed_chararcters.replace(character, '')

        for character in disallowed_chararcters:
            field = field.replace(character, '')

        return field

    def initialise_metadata(self) -> None:
        """Initalise attributes relevant to metadata."""
        self.metadata = None

    def initialise_monthly_data(self) -> None:
        """Initialise attrributes relevant to monthly data."""
        self.month = None
        self.tmax = None
        self.tmax_is_estimated = None
        self.tmin = None
        self.tmin_is_estimated = None
        self.af = None
        self.af_is_estimated = None
        self.rain = None
        self.rain_is_estimated = None
        self.sun = None
        self.sun_is_estimated = None
        self.sun_instrument = None
        self.provisional = None

    def parse_field(self, field: str, func: object) -> tuple:
        """
        Parse an individual field.

        Parameters
        ----------
        field : str
            The field to be parsed.

        func : function
            The numeric function (e.g. float or int) to parse the field.

        Returns
        -------
        tuple
            Contains two elements, the first is float, the second is a bool.
        """
        if field == '---':
            return (None, None)
        is_estimated = False

        if field.endswith('*'):
            is_estimated = True
            field = field.removesuffix('*')

        return (func(field), is_estimated)

    def parse_line(self) -> None:
        """Parse the input line."""
        stripped_line = self.line.strip()

        if (not self.line.startswith(' ')) or stripped_line[0].isalpha():
            self.metadata = stripped_line
            return

        line = stripped_line
        self.provisional = False

        if line.endswith('Provisional'):
            self.provisional = True
            line.replace('Provisional', '')

        prog = re.compile('[ \t\n\r]+')
        fields = prog.split(line)

        field = fields.pop(0)
        (year, null) = self.parse_field(field, int)
        field = fields.pop(0)
        (month, null) = self.parse_field(field, int)
        self.month = f'{year:04d}-{month:02d}'

        field = fields.pop(0)
        (self.tmax, self.tmax_is_estimated) = self.parse_field(field, float)

        field = fields.pop(0)
        (self.tmin, self.tmin_is_estimated) = self.parse_field(field, float)

        field = fields.pop(0)
        (self.af, self.af_is_estimated) = self.parse_field(field, int)

        field = fields.pop(0)
        (self.rain, self.rain_is_estimated) = self.parse_field(field, float)

        if len(fields) == 0:
            # In March 1945, Lowestoft had no data for sun, but didn't add
            # the no data field.  We fix that here.
            fields = ['---']

        field = fields.pop(0)
        (field, self.sun_instrument) = self.parse_sun_instrument(field)
        (self.sun, self.sun_is_estimated) = self.parse_field(field, float)

    def parse_sun_instrument(self, field: str) -> tuple:
        """
        Parse the sun instrument type from a string field.

        Parameters
        ----------
        field : str
            The field to be parsed.

        Returns
        -------
        tuple
            The first element is a string containing the new field, the second
            is a string and is the name of the sun instrument.
        """
        if field == '---':
            return ('---', None)

        field = self.clean_sun_field(field)

        if field.endswith('#'):
            sun_instrument = 'Kipp & Zonen sensor'
            field = field.removesuffix('#')
        elif field.endswith('*'):
            sun_instrument = None
        else:
            sun_instrument = 'Campbell Stokes recorder'

        return (field, sun_instrument)

    def to_dict(self) -> dict:
        """
        Return the parsed line as a dict.

        Returns
        -------
        dict
            A dictionary containing the fields extracted from the input line.
        """
        return {
            'station_name': self.station_name,
            'line': self.line,
            'metadata': self.metadata,
            'month': self.month,
            'tmax': self.tmax,
            'tmax_is_estimated': self.tmax_is_estimated,
            'tmin': self.tmin,
            'tmin_is_estimated': self.tmin_is_estimated,
            'af': self.af,
            'af_is_estimated': self.af_is_estimated,
            'rain': self.rain,
            'rain_is_estimated': self.rain_is_estimated,
            'sun': self.sun,
            'sun_is_estimated': self.sun_is_estimated,
            'sun_instrument': self.sun_instrument,
            'provisional': self.provisional
        }
