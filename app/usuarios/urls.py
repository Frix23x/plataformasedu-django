from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.static import serve

from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'), # Ruta para registro
    path('login/', views.login_view, name='login'), # Ruta para login
    path('panel-profesor/', views.panel_profesor, name='panel_profesor'), # Para profesores
    path('panel-estudiante/', views.panel_estudiante, name='panel_estudiante'), # Para estudiantes
    path('inscribirse/<int:curso_id>/', views.inscribirse, name='inscribirse'), # Para inscribirse
    path('evaluaciones/', views.evaluaciones_estudiante, name='evaluaciones_estudiante'), # Para las evaluaciones
    path('crear-evaluacion/', views.crear_evaluacion, name='crear_evaluacion'), # Para crear las evaluaciones
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), # Para cerrar sesión
    path('evaluacion/<int:evaluacion_id>/editar/', views.editar_evaluacion, name='editar_evaluacion'), # Para editar evaluacion
    path('evaluacion/<int:evaluacion_id>/eliminar/', views.eliminar_evaluacion, name='eliminar_evaluacion'), # Para eliminar evaluacion
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)