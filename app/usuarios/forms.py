from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .models import Evaluacion

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'password1', 'password2']

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['curso', 'titulo', 'descripcion', 'fecha']
