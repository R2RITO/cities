"""
View used to ingest private taxi trip data uploaded through a file.
The data should have the latitude and longitude of a trip identified by
unique key, and this ingest process appends the human readable location fix,
removes duplicates and uploads the data to the data warehouse.
"""
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from private_ingest.serializers.private_source_ingest_serializer import (
    PrivateSourceIngestSerializer)
from dask import dataframe as dd
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from private_ingest.utils.location_fix import add_location_fix
from dw_storage.utils.bq_utils import upload_private_source_results_to_bq
from datetime import datetime
from django.conf import settings
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


class PrivateSourceIngestView(views.APIView):

    @swagger_auto_schema(
        request_body=PrivateSourceIngestSerializer,
        responses={204: "Succesfully uploaded data"}
    )
    def post(self, request, **kwargs):
        """
        Parse the uploaded CSV file, retrieve the location fix of the
        coordinates and upload the results to the data warehouse in BigQuery
        """
        serializer = PrivateSourceIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """
        Process the file into a dataframe, remove duplicates and add a new
        column containing the human readable location fix value
        """
        try:
            filename = request.FILES['data_file'].temporary_file_path()
            df = dd.read_csv(
                filename,
                dtype={
                    "trip_id": str,
                    "latitude": float,
                    "longitude": float
                }
            )
            df = df.drop_duplicates()
            df['location_fix'] = df.apply(
                func=add_location_fix,
                axis=1,
                meta=('location_fix', str)
            )

            """
            The duplicate rows are removed because they do not add value to
            the dataset. Furthermore, there might be some invalid rows, such
            as rows with invalid latitude and longitude values, or rows with
            valid values but impossible locations (such a taxi trip over the
            ocean). To filter this, when the geocoding fails, the row is
            removed since the location fix is required
            """
            df = df[
                (df.longitude <= 90.0) &
                (df.longitude >= -90.0) &
                (df.latitude <= 180.0) &
                (df.latitude >= -180.0) &
                df.location_fix
            ]

        except ValueError as e:
            data = {
                'message': "Error decoding CSV file"
            }
            logger.error(str(e))
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except (HTTPError, ConnectionError) as e:
            data = {
                'message': "Error processing CSV data"
            }
            logger.error(str(e))
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        """
        When a chunk is ingested, the resulting data has to be uploaded,
        if there is an error uploading to the data warehouse, store the
        content in a file and notify via email to issue reuploading
        when the service is available.
        """
        try:
            table = settings.TAXI_TRIPS_DETAILS_TABLE
            upload_private_source_results_to_bq(df.compute(), table)

        except Exception as e:
            """
            Store both the processed dataframe and the original csv file for
            manual review and correction
            """
            logger.error(str(e))

            filename = datetime.now().strftime('%d-%m-%Y_%H%M%S') + '.parquet'
            filepath = Path(settings.FAILED_UPLOADS_DIR) / filename
            df.to_parquet(filepath, engine='pyarrow')

            filename = datetime.now().strftime('%d-%m-%Y_%H%M%S') + '.csv'
            filepath = Path(settings.FAILED_UPLOADS_DIR) / filename
            data_file = request.data.get('data_file')
            with open(filepath, 'wb+') as destination:
                for chunk in data_file.chunks():
                    destination.write(chunk)

            data = {
                'message': "Error uploading processed CSV data"
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)
