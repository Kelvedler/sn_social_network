from django.db.models import Q
from django.urls import path
from rest_framework import viewsets, serializers, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from person.models import PostLike, Person


class AnalyticsSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, attrs):
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        if date_from and date_to and date_from > date_to:
            raise exceptions.ValidationError('date_from after date_to')
        return attrs


class LikesViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['get'])
    def analytics(self, request):
        serializer = AnalyticsSerializer(data=request.query_params)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')
        qs_filter = Q()
        if date_from:
            qs_filter &= Q(created_at__date__gte=date_from)
        if date_to:
            qs_filter &= Q(created_at__date__lte=date_to)
        likes_count = PostLike.objects.filter(qs_filter).count()
        return Response({'likes': likes_count}, status=200)


class PersonActivityViewSet(viewsets.ViewSet):

    def retrieve(self, request, person_id=None):
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            raise exceptions.NotFound()
        return Response(person.as_activity_dict(), status=200)


urlpatterns = [
    path('likes', LikesViewSet.as_view({'get': 'analytics'})),
    path('persons/<uuid:person_id>/activity', PersonActivityViewSet.as_view({'get': 'retrieve'}))
]
