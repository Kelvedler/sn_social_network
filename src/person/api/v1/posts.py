from django.urls import path
from rest_framework import viewsets, serializers as rest_framework_serializers, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from main.serializers import PageSerializer
from main.utils.pagination import fetch_list
from person.models import Post, Person, PostLike
from person.serializers import PostModelSerializer


class PostsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = Post.objects.all()
        serializer = PageSerializer(data=request.query_params)
        if not serializer.is_valid():
            raise rest_framework_serializers.ValidationError(serializer.errors)
        page = serializer.validated_data.get('page') or 0
        total, pages, posts = fetch_list(queryset, page)
        caller = request.user if isinstance(request.user, Person) else None
        return Response({
            'total': total,
            'pages': pages,
            'posts': [post.as_dict(caller) for post in posts]
        }, status=200)

    def create(self, request):
        request.data['person'] = request.user.id
        serializer = PostModelSerializer(data=request.data)
        if not serializer.is_valid():
            raise rest_framework_serializers.ValidationError(serializer.errors)
        post = serializer.create(serializer.validated_data)
        return Response(post.as_dict(request.user), status=201)


class PostsLikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, post_id=None):
        caller = request.user
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound()
        try:
            like = post.likes.get(person=caller)
        except PostLike.DoesNotExist:
            PostLike.objects.create(post=post, person=caller)
        else:
            like.delete()
        return Response(post.as_dict(caller), status=200)


urlpatterns = [
    path('', PostsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<uuid:post_id>/like', PostsLikeViewSet.as_view({'post': 'like'}))
]
