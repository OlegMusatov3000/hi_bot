from django.urls import path

from .views import UserViewSet

urlpatterns = [
    path(
        'filter/',
        UserViewSet.as_view({'get': 'list'}),
        name='filter'
    )
]