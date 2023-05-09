from django.urls import path, include
from . import sign_up, sign_in, refresh, posts

urlpatterns = [
    path('sign-up', include(sign_up.urlpatterns)),
    path('sign-in', include(sign_in.urlpatterns)),
    path('refresh', include(refresh.urlpatterns)),
    path('posts/', include(posts.urlpatterns)),
]
