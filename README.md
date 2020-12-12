# cities

# About

This is a showcase project, used to retrieve data from two different sources
and upload it to GCP's BigQuery service


# Setup

## Clone
Clone the project

    git clone https://github.com/R2RITO/cities.git

## Virtualenv
Use a python 3 virtual environment, for example:

    virtualenv -p python3 venv
    source venv/bin/activate

## Environment variables
Set up the environment variables

    ALLOWED_HOSTS
    LOG_FILE_PATH
    GOOGLE_APPLICATION_CREDENTIALS
    GOOGLE_CLOUD_PROJECT
    TAXI_TRIPS_DETAILS_TABLE
    TAXI_TRIPS_INGESTED_DETAILS_TABLE
    TAXI_TRIPS_TABLE
    FAILED_UPLOADS_DIR
    
Example:

    export ALLOWED_HOSTS='*'
    export LOG_FILE_PATH='/home/fulanito/Projects/cities/logs'
    export GOOGLE_APPLICATION_CREDENTIALS='/home/fulanito/Projects/cities/project_creds.json'
    export GOOGLE_CLOUD_PROJECT='project_id'
    export TAXI_TRIPS_DETAILS_TABLE='cities.taxi_trips_details'
    export TAXI_TRIPS_INGESTED_DETAILS_TABLE='cities.taxi_trips_ingested_details'
    export TAXI_TRIPS_TABLE='cities.taxi_trips'
    export FAILED_UPLOADS_DIR='/home/fulanito/Projects/cities/failed_uploads'

## Requirements
Install the requirements

    pip install -r requirements/prod.txt
    
## Tests
Run tests

    python manage.py test private_ingest.tests

## Run 

    python manage.py runserver


## Documentation

The folder openapi contains a swagger.yml file, following the OpenApi 2.0
specification, that documents the endpoints exposed in this project. To
use it, the file should be loaded into an OpenApi visualizer such as the
one provided in https://editor.swagger.io/ in order to explore the
services.

When an endpoint is updated, the file should be re-generated using the
command

    python manage.py generate_swagger swagger.yaml

And then, moved to the openapi folder, this will allow for the version control
to display the changes and allow for editing unwanted changes

As additional notes, the examples are defined in the serializers of each
resource, and some of them require the readOnly: true attribute to be set
manually after generating the file.
    
## Obfuscation

The file cython_setup.py has the required setup to compile most of the
source files into .so files, useful to deploy on a server where the code
is going to be used but should not be available for inspection.

To compile the project, run the command:

    python cython_setup.py build_ext

This will create a folder called build, inside of which the compiled
project will be located, then, the required files can be moved to the
desired project location and the project can be run as normal with the
compiled files.

When a new directory, or file that requires special attention is created,
the cython_setup.py file should be updated to include it in the compiled
sources.
