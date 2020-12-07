"""
Module used to provide BQ functions that allow the suite to query or
upload data
"""
from google.cloud import bigquery


def upload_private_source_results_to_bq(df, table):
    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("location_fix", "STRING"),
    ])

    return upload_results_to_bq(df, table, job_config)


def upload_chicago_dataset_results_to_bq(df, table):
    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("pickup_location_fix", "STRING"),
        bigquery.SchemaField("dropoff_location_fix", "STRING"),
    ])

    return upload_results_to_bq(df, table, job_config)


def upload_results_to_bq(df, table, job_config=None):
    """
    Function that takes a dataframe containing data for the taxi_trips_details
    table, and uploads it to BQ
    :param DataFrame df: dask/pandas dataframe with the data
    :param str table: table name on the BQ platform
    :param JobConfig job_config: job config to upload the data
    :return:
    """
    client = bigquery.Client()
    table_id = table

    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )

    # Wait for the load job to complete.
    job.result()
