from django.urls import path, include
from . import analytics

urlpatterns = [
    path('analytics/', include(analytics.urlpatterns))
]
