"""
Module used to test the
utils/location_fix/add_location_fix function,
used to apply reverse geocoding to the coordinates and retrieve the human
readable location name.
"""
from private_ingest.utils.location_fix import add_location_fix
from django.test import TestCase
from unittest.mock import patch


class AddLocationFixTest(TestCase):

    @patch('private_ingest.utils.location_fix.get_location_fix_by_coordinates')
    def test_add_location_fix(self, mocked_get_location_fix):
        params = {
            'latitude': 54.9824031826,
            'longitude': 9.283268,
        }
        add_location_fix(params)

        assert mocked_get_location_fix.called_once
