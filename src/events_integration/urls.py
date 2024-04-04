from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .rest.views.event import EventsView

app_name = 'events_integration'

router = DefaultRouter()

router.register(r'events/search', EventsView, basename='events')

urlpatterns = [
    path('', include(router.urls)),
]
