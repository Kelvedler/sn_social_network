from django.urls import path
from rest_framework import viewsets, serializers as rest_framework_serializers
from rest_framework.response import Response

from main.utils.jwt_ import encode_access, encode_refresh
from person.serializers import PersonModelSerializer


class SignUpViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = PersonModelSerializer(data=request.data)
        if not serializer.is_valid():
            raise rest_framework_serializers.ValidationError(serializer.errors)
        person = serializer.create(serializer.validated_data)
        return Response({
            'access_token': encode_access(person.id),
            'refresh_token': encode_refresh(person.id)
        }, status=200)


urlpatterns = [
    path('', SignUpViewSet.as_view({'post': 'create'}))
]
