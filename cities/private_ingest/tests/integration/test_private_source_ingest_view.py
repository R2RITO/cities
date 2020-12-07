"""
Module used to test the PrivateSourceIngest view, with all the available
operations
"""
from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class PrivateSourceIngestTest(TestCase):
    def setUp(self) -> None:
        # CSV file setup
        self.data_file = (
            settings.BASE_DIR /
            'private_ingest/tests/fixtures/test_data_file.csv'
        )

    def test_process_correct_data_file(self):

        with open(self.data_file, 'rb') as data_file:
            params = {
                'data_file': data_file,
            }
            result = self.client.post(
                reverse('private_source_ingest-list'),
                data=params
            )

        assert result.status_code == 204
