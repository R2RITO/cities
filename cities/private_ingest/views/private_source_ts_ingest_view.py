"""
View used to ingest private taxi trip data queried from the Chicago taxi
trips public dataset.
"""
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from google.cloud import bigquery
from django.conf import settings
import logging


logger = logging.getLogger(__name__)
TABLE_ID = '.'.join([
    settings.GOOGLE_CLOUD_PROJECT,
    settings.TAXI_TRIPS_INGESTED_DETAILS_TABLE
    ]
)


class PrivateSourceTSIngestView(views.APIView):

    @swagger_auto_schema(
        request_body=None,
        responses={204: ""}
    )
    def post(self, request, **kwargs):
        """
        Query the private datasets, and upload retrieved data to the data
        warehouse on BigQuery after performing the desired JOIN operation
        """
        try:
            client = bigquery.Client()
            job_config = bigquery.QueryJobConfig(destination=TABLE_ID)

            sql = """
                SELECT 
                t.taxi_id, t.latitude, t.longitude, t.location_fix, 
                tr.unique_key as trip_id, t.timestamp 
                FROM 
                `cast-297716.cities.taxi_trips_details` as t 
                LEFT JOIN 
                `cast-297716.cities.taxi_trips` as tr 
                ON t.taxi_id = tr.taxi_id 
                WHERE 
                t.timestamp >= tr.trip_start_timestamp 
                AND 
                t.timestamp <= tr.trip_end_timestamp
            """
            query_job = client.query(sql, job_config=job_config)
            query_job.result()

        except Exception as e:
            data = {
                'message': "Error retrieving/uploading relationship data"
            }
            logger.error(str(e))
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)
