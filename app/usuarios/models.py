# models.py
# Este archivo define la estructura de las tablas que se crearán en la base de datos
# Cada clase representa un modelo (una tabla), y cada atributo una columna.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Usado para referenciar AUTH_USER_MODEL sin importar su nombre

# 👤 Modelo de usuario personalizado (hereda de AbstractUser)
class Usuario(AbstractUser):
    # Opciones de rol para el usuario
    ROL_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    )

    # Campo adicional 'rol' para diferenciar entre tipos de usuario
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')

    # Representación en texto para panel de admin y consola
    def __str__(self):
        return f"{self.username} ({self.rol})"

# 📚 Modelo de Curso
class Curso(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del curso
    descripcion = models.TextField()           # Descripción larga
    profesor = models.ForeignKey(              # Relación con el modelo Usuario (solo profesores)
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'profesor'}   # Solo usuarios con rol 'profesor'
    )

    def __str__(self):
        return self.nombre

# 🧑‍🎓 Modelo de Inscripción a un curso
class Inscripcion(models.Model):
    estudiante = models.ForeignKey(            # Relación con el usuario (solo estudiantes)
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'estudiante'}
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Curso al que se inscribe
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)  # Fecha automática al crearse

    class Meta:
        unique_together = ('estudiante', 'curso')  # Evita inscripciones duplicadas

    def __str__(self):
        return f"{self.estudiante.username} inscrito en {self.curso.nombre}"

# 📝 Modelo de Evaluación de un curso
class Evaluacion(models.Model):
    curso = models.ForeignKey(                        # Curso relacionado
        Curso,
        on_delete=models.CASCADE,
        related_name='evaluaciones'                   # Permite acceder con curso.evaluaciones.all()
    )
    titulo = models.CharField(max_length=100)         # Título de la evaluación
    descripcion = models.TextField()                  # Descripción o detalles
    fecha = models.DateField()                        # Fecha programada de la evaluación

    def __str__(self):
        return f"{self.titulo} - {self.curso.nombre}"
