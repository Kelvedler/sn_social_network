from rest_framework import serializers


class PageSerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=0, required=False)
