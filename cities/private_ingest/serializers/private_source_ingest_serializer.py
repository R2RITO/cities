from rest_framework import serializers


class PrivateSourceIngestSerializer(serializers.Serializer):
    data_file = serializers.FileField(required=True)
