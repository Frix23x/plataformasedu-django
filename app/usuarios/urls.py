from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'), # Ruta para login
    path('panel-profesor/', views.panel_profesor, name='panel_profesor'), # Para profesores
    path('panel-estudiante/', views.panel_estudiante, name='panel_estudiante'), # Para estudiantes
    path('inscribirse/<int:curso_id>/', views.inscribirse, name='inscribirse'),
]
