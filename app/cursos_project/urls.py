from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
]

# 🧩 Solo en desarrollo: sirve archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 🧩 Para evitar el error 404 del favicon
urlpatterns += [
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': settings.BASE_DIR}),
]
