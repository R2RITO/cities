"""
private_ingest app URLs
"""
from django.urls import path
from private_ingest.views.private_source_ingest_view import (
    PrivateSourceIngestView)
from private_ingest.views.private_source_ts_ingest_view import (
    PrivateSourceTSIngestView)


urlpatterns = [
    path(
        'private_source_ingest',
        PrivateSourceIngestView.as_view(),
        name='private_source_ingest-list'
    ),
    path(
        'private_source_ts_ingest',
        PrivateSourceTSIngestView.as_view(),
        name='private_source_ts_ingest-list'
    ),
]
