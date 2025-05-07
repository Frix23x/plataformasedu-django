from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .models import Curso
from .models import Inscripcion
from .models import Evaluacion

# Admin para el modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )
    list_display = ['username', 'email', 'rol', 'is_staff']

# Admin básico para el modelo Curso
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'profesor']
    search_fields = ['nombre']

admin.site.register(Inscripcion)

# Admin para el modelo Evaluacion
@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'fecha']