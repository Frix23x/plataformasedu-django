# admin.py
# Este archivo sirve para personalizar cómo se visualizan y administran los modelos
# desde el panel de administración de Django (/admin).

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Clase base para personalizar usuarios
from .models import Usuario                     # Modelo de usuario personalizado
from .models import Curso                       # Modelo de curso
from .models import Inscripcion                 # Modelo de inscripción
from .models import Evaluacion                  # Modelo de evaluación

# 🧑‍💻 Admin personalizado para el modelo Usuario (hereda de UserAdmin)
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Añadimos el campo "rol" a la sección de campos adicionales en el formulario de admin
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )
    # Columnas visibles en la tabla de usuarios en el panel de administración
    list_display = ['username', 'email', 'rol', 'is_staff']

# 📚 Admin personalizado para el modelo Curso
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'profesor']       # Columnas mostradas en la tabla de cursos
    search_fields = ['nombre']                  # Campo de búsqueda en el admin

# 👥 Registro simple de Inscripcion (sin personalización especial)
admin.site.register(Inscripcion)

# 📄 Admin personalizado para el modelo Evaluacion
@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'fecha']  # Columnas mostradas para evaluaciones
