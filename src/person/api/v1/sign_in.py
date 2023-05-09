from django.urls import path
from rest_framework import viewsets, exceptions, serializers as rest_framework_serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from main.utils.jwt_ import encode_access, encode_refresh
from main.utils.time import get_now
from person.serializers import PersonSerializer


class SignInViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['post'])
    def sign_in(self, request):
        serializer = PersonSerializer(data=request.data)
        if not serializer.is_valid():
            raise rest_framework_serializers.ValidationError(serializer.errors)
        person = serializer.get_from_credentials(serializer.validated_data)
        if not person:
            raise exceptions.AuthenticationFailed()
        person.last_login = get_now()
        person.save()
        return Response({
            'access_token': encode_access(person.id),
            'refresh_token': encode_refresh(person.id)
        }, status=200)


urlpatterns = [
    path('', SignInViewSet.as_view({'post': 'sign_in'}))
]
