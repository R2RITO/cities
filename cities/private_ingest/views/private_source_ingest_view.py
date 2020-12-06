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
from dw_storage.utils.bq_utils import upload_results_to_bq


class PrivateSourceIngestView(views.APIView):

    @swagger_auto_schema(
        request_body=PrivateSourceIngestSerializer,
        responses={204: None}
    )
    def post(self, request, format=None):
        serializer = PrivateSourceIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """
        Process the file into a dataframe, remove duplicates and add a new
        column containing the human readable location fix value
        """
        try:
            filename = request.FILES['data_file'].temporary_file_path()
            df = dd.read_csv(filename)
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
                'message': e
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except (HTTPError, ConnectionError) as e:
            data = {
                'message': e
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        """
        When a chunk is ingested, the resulting data has to be uploaded,
        if there is an error uploading to the data warehouse, store the
        content in a file and notify via email to issue reuploading
        when the service is available.
        """
        try:
            upload_results_to_bq(df)
        except Exception as e:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
