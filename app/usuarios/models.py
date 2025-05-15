# models.py
# Este archivo define la estructura de las tablas que se crearán en la base de datos
# Cada clase representa un modelo (una tabla), y cada atributo una columna.

from django.conf import settings  # Para referenciar AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
from django.core.validators import \
    FileExtensionValidator  # Para validar archivos PDF
from django.db import models


# 👤 Modelo de usuario personalizado
class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')

    def __str__(self):
        return f"{self.username} ({self.rol})"

# 📚 Modelo de curso asignado a un profesor
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'profesor'}
    )

    def __str__(self):
        return self.nombre

# 🧑‍🎓 Modelo de inscripción a cursos
class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'estudiante'}
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('estudiante', 'curso')

    def __str__(self):
        return f"{self.estudiante.username} inscrito en {self.curso.nombre}"

# 📝 Modelo de evaluación con PDF opcional
class Evaluacion(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='evaluaciones'
    )
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()

    # ✅ Campo para archivo PDF (opcional)
    archivo_pdf = models.FileField(
        upload_to='evaluaciones_pdfs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])],
        verbose_name='Archivo PDF'
    )

    def __str__(self):
        return f"{self.titulo} - {self.curso.nombre}"

    # ✅ Si se elimina una evaluación, también se elimina su archivo PDF
    def delete(self, *args, **kwargs):
        if self.archivo_pdf:
            self.archivo_pdf.delete(save=False)
        super().delete(*args, **kwargs)
