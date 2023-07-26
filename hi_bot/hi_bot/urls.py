from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# Переопределяем хендлеры.
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

urlpatterns = [
    # Добавляем пространство имён из приложения 'message'.
    path('', include('message.urls', namespace='message')),
    # Добавляем пространство имён из приложения 'about'.
    path('about/', include('about.urls', namespace='about')),
    path('admin/', admin.site.urls),
    # Добавляем пространство имён из приложения 'users'.
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
]

# Добавляем автоматическое формирование документации.
schema_view = get_schema_view(
   openapi.Info(
      title="Hibot",
      default_version='v1',
      description="Документация для приложения api проекта Hibot",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="admin@kittygram.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]

# Если DEBUG=True брать картинки из директории, указанной в MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
