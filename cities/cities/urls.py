"""
cities URL Configuration
"""
from private_ingest.urls import urlpatterns as private_ingest_urls
from chicago_ingest.urls import urlpatterns as chicago_ingest_urls
from drf_yasg import openapi


schema_info = openapi.Info(
      title="Cities API",
      default_version='v1',
      description="API used to ingest data from the Chicago Taxi Trips"
                  "database and independent sources",
)

urlpatterns = []

urlpatterns.extend(private_ingest_urls)
urlpatterns.extend(chicago_ingest_urls)
