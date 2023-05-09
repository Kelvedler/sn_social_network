from django.urls import path
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.utils.jwt_ import TYPE_REFRESH, encode_access, InvalidToken


class RefreshViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def refresh(self, request):
        if request.auth.get('type') != TYPE_REFRESH:
            raise InvalidToken()
        return Response({'access_token': encode_access(request.auth.get('id'))}, status=200)


urlpatterns = [
    path('', RefreshViewSet.as_view({'post': 'refresh'}))
]
