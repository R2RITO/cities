"""
chicago_ingest app URLs
"""
from django.urls import path
from chicago_ingest.views.chicago_dataset_ingest_view import (
    ChicagoDatasetIngestView)


urlpatterns = [
    path(
        'chicago_dataset_ingest',
        ChicagoDatasetIngestView.as_view(),
        name='chicago_dataset_ingest-list'
    ),
]
