from django.urls import path, include

app_name = 'api'

urlpatterns = [
    # Если апи v1 то ищем в api.v1.urls.
    path('v1/', include('api.v1.urls')),
]
