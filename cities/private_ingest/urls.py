"""
private_ingest app URLs
"""
from django.urls import path
from private_ingest.views.private_source_ingest_view import (
    PrivateSourceIngestView)


urlpatterns = [
    path(
        'private_source_ingest',
        PrivateSourceIngestView.as_view(),
        name='private_source_ingest-list'
    ),
]
