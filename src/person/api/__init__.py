from django.urls import path, include
from . import v1

urlpatterns = [
    path('v1/', include(v1.urlpatterns))
]
