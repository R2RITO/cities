"""
Module that provides functions used to get a location fix given
partial data
"""
import requests


SERVICE_URL = 'http://nominatim.openstreetmap.org/reverse'
'?format=json&lat=54.9824031826&lon=9.2833114795&zoom=18&addressdetails=1'


def get_location_fix_by_coordinates(latitude, longitude):
    """
    Function used to get the human readable name of a location
    given the latitude and longitude coordinates
    :param float latitude: latitude angle
    :param float longitude: longitude angle
    :return str: Human readable name of the location
    :raises ConnectionError: on error fetching the location
    :raises HTTPError: on error fetching the location
    """

    params = {
        'format': 'json',
        'lat': latitude,
        'lon': longitude,
    }
    name = ''

    result = requests.get(url=SERVICE_URL, params=params)

    if str(result.status_code).startswith('2'):
        name = result.json().get('display_name', '')

    return name


def add_location_fix(row):
    return get_location_fix_by_coordinates(
        row['latitude'], row['longitude']
    )


def add_custom_location_fix(row, column_name):
    return get_location_fix_by_coordinates(
        row[column_name + '_latitude'], row[column_name + '_longitude']
    )
