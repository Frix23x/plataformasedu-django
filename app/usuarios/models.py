from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings   # Importante para usar AUTH_USER_MODEL

# Modelo de usuario personalizado
class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    )

    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')

    def __str__(self):
        return f"{self.username} ({self.rol})"

# Modelo de curso relacionado a profesores
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'profesor'}
    )

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'estudiante'}
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('estudiante', 'curso')  # evita inscripciones duplicadas

    def __str__(self):
        return f"{self.estudiante.username} inscrito en {self.curso.nombre}"

    def __str__(self):
        return self.nombre
    
class Evaluacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='evaluaciones')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.curso.nombre}"

