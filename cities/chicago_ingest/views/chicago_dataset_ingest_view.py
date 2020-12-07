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


class ChicagoDatasetIngestView(views.APIView):

    @swagger_auto_schema(
        request_body=None,
        responses={204: None}
    )
    def post(self, request, **kwargs):
        """
        Query the public dataset, and upload retrieved data to the data
        warehouse on bq
        """
        try:
            client = bigquery.Client()
            project = settings.GOOGLE_CLOUD_PROJECT
            table = settings.TAXI_TRIPS_TABLE
            destination = '.'.join([project, table])
            job_config = bigquery.QueryJobConfig(
                destination=destination,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
            )
            sql = """
                SELECT *
                FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                WHERE 
                pickup_latitude is not null AND
                pickup_longitude is not null AND
                dropoff_latitude is not null AND
                dropoff_longitude is not null
                LIMIT 100
            """
            query_job = client.query(sql, job_config=job_config)
            query_job.result()

        except Exception as e:
            data = {
                'message': e
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)
