from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

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

# Если DEBUG=True брать картинки из директории, указанной в MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
