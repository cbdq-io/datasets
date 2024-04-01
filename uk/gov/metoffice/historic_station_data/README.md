# Met Offoce Historical Station Data

A dataset wrangled from the UK Met Office and available at
<https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data>.

## Fields

1. station_name: The name of the station that the data refers to.
1. metadata: Free text associated with the station.  Will be blank if the row is for a data record.
1. month:  The [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) month (e.g. 2024-04).  Will be blank if the row is a data record.
1. tmax: Mean daily maximum temperature (centigrade).  Will be blank if month is blank or no data is available.
1. tmax_is_estimated: True if tmax is estimated, false if is estimated, blank if tmax or month is absent.
1. tmin
1. tmin_is_estimated: True if tmin is estimated, false if is not estimated, blank if tmin or month is absent.
1. af: Days of air frost.  Will be blank if month is blank for no data is available.
1. af_is_estimated: True if af is estimated, false if is not estimated, blank if af or main is absent.
1. rain: Rainfall (mm).  Will be blank if month is blank or no rain data is available.
1. rain_is_estimated: True if rain is estimated, false if is not estimated, blank if rain or main is absent.
1. sun: The number of hours of sunshine.  Will be blank if month is blank or no sun data is available.
1. sun_is_estimated: True if sun is estimated, false if is not estimated, blank if sun or main is absent.
1. sun_instrument: The sun instrument (blank if unavailable).  Will either be Campbell-Stokes recorder or Campbell-Stokes recorder.
1. provisional: Data are indicated as provisional until the full network quality control has been carried out. After this, data are final.
