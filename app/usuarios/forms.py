# forms.py
# Este archivo define formularios personalizados que se conectan con tus modelos.
# Django los usará para renderizar formularios en HTML, validar campos y guardar datos.

from django import forms
from django.contrib.auth.forms import UserCreationForm  # Formulario base para registrar usuarios con contraseña
from .models import Usuario                              # Modelo personalizado de usuario
from .models import Evaluacion                           # Modelo de evaluaciones

# 🧑‍💻 Formulario para registrar nuevos usuarios
class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario  # Usa el modelo personalizado 'Usuario'
        fields = ['username', 'email', 'rol', 'password1', 'password2']
        # Estos son los campos que se mostrarán en el formulario de registro:
        # - username: nombre de usuario
        # - email: correo electrónico
        # - rol: campo personalizado (estudiante, profesor, admin)
        # - password1 y password2: contraseña y confirmación

# 📝 Formulario para que los profesores creen nuevas evaluaciones
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion  # Se basa en el modelo Evaluacion
        fields = ['curso', 'titulo', 'descripcion', 'fecha']
        # Campos del formulario:
        # - curso: curso al que pertenece
        # - titulo: nombre de la evaluación
        # - descripcion: detalles o instrucciones
        # - fecha: fecha programada
