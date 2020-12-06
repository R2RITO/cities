"""
Module used to provide BQ functions that allow the suite to query or
upload data
"""
from google.cloud import bigquery
from django.conf import settings


def upload_results_to_bq(df):
    """
    Function that takes a dataframe containing data for the taxi_trips_details
    table, and uploads it to BQ
    :param DataFrame df: dask/pandas dataframe with the data
    :return:
    """
    client = bigquery.Client()
    table_id = settings.TAXI_TRIPS_DETAILS_TABLE

    # Since string columns use the "object" dtype, pass in a (partial) schema
    # to ensure the correct BigQuery data type.
    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("location_fix", "STRING"),
    ])

    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )

    # Wait for the load job to complete.
    job.result()
