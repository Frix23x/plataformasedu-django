from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from .models import Curso, Inscripcion
from django.views.decorators.http import require_POST

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirige a la vista login_view
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# Vista de login con redirección por rol
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            # Redirigir según rol
            if usuario.rol == 'admin':
                return redirect('/admin/')
            elif usuario.rol == 'profesor':
                return redirect('/panel-profesor/')
            else:
                return redirect('/panel-estudiante/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

# Vista real de panel profesor con cursos asignados
@login_required
def panel_profesor(request):
    cursos = Curso.objects.filter(profesor=request.user)
    return render(request, 'panel_profesor.html', {'cursos': cursos})

# Igualmente con los estudiantes
@login_required
def panel_estudiante(request):
    cursos = Curso.objects.all()
    cursos_inscritos = Inscripcion.objects.filter(estudiante=request.user).values_list('curso_id', flat=True)
    return render(request, 'panel_estudiante.html', {
        'cursos': cursos,
        'cursos_inscritos': cursos_inscritos
    })

@login_required
@require_POST
def inscribirse(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    # Verifica si ya está inscrito
    ya_inscrito = Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists()

    if not ya_inscrito:
        Inscripcion.objects.create(estudiante=request.user, curso=curso)
    
    return redirect('panel_estudiante')
