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
from private_ingest.utils.location_fix import add_custom_location_fix
from dw_storage.utils.bq_utils import upload_chicago_dataset_results_to_bq


logger = logging.getLogger(__name__)


class ChicagoDatasetIngestView(views.APIView):

    @swagger_auto_schema(
        request_body=None,
        responses={204: "Succesfully uploaded data"}
    )
    def post(self, request, **kwargs):
        """
        Query the public dataset, and upload retrieved data to the data
        warehouse on BigQuery
        """
        try:
            client = bigquery.Client()

            sql = """
                SELECT
                unique_key,
                taxi_id,
                trip_start_timestamp,
                trip_end_timestamp,
                trip_seconds,
                trip_miles,
                pickup_latitude,
                pickup_longitude,
                dropoff_latitude,
                dropoff_longitude
                FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
                WHERE 
                pickup_latitude is not null AND
                pickup_longitude is not null AND
                dropoff_latitude is not null AND
                dropoff_longitude is not null
                LIMIT 5
            """
            query_job = client.query(sql)
            df = query_job.to_dataframe()

            df['pickup_location_fix'] = df.apply(
                func=add_custom_location_fix,
                axis=1,
                args=('pickup',)
            )
            df['dropoff_location_fix'] = df.apply(
                func=add_custom_location_fix,
                axis=1,
                args=('dropoff',)
            )

            """
            Upload results to data warehouse
            """
            table = settings.TAXI_TRIPS_TABLE
            upload_chicago_dataset_results_to_bq(df, table)

        except Exception as e:
            data = {
                'message': "Error retrieving/uploading public data"
            }
            logger.error(str(e))
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)
