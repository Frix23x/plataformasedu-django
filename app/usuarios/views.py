from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import RegistroForm
from .forms import EvaluacionForm
from .models import Curso, Inscripcion, Usuario
from .models import Evaluacion


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
    profesor = request.user

    # Cursos que dicta el profesor
    cursos = Curso.objects.filter(profesor=profesor)

    # Para cada curso, obtener sus estudiantes inscritos
    cursos_con_estudiantes = []
    for curso in cursos:
        estudiantes = Usuario.objects.filter(inscripcion__curso=curso)
        cursos_con_estudiantes.append((curso, estudiantes))

    return render(request, 'panel_profesor.html', {
        'cursos_con_estudiantes': cursos_con_estudiantes
    })

# Igualmente con los estudiantes
@login_required
def panel_estudiante(request):
    usuario = request.user

    # Cursos en los que ya está inscrito
    cursos_inscritos = Curso.objects.filter(inscripcion__estudiante=usuario)

    # Cursos en los que aún NO está inscrito
    cursos_disponibles = Curso.objects.exclude(inscripcion__estudiante=usuario)

    return render(request, 'panel_estudiante.html', {
        'cursos_disponibles': cursos_disponibles,
        'cursos_inscritos': cursos_inscritos,
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

@login_required
def evaluaciones_estudiante(request):
    usuario = request.user

    # Cursos donde el estudiante está inscrito
    cursos_inscritos = Curso.objects.filter(inscripcion__estudiante=usuario)

    # Evaluaciones de esos cursos
    evaluaciones = Evaluacion.objects.filter(curso__in=cursos_inscritos).order_by('fecha')

    return render(request, 'evaluaciones_estudiante.html', {
        'evaluaciones': evaluaciones
    })

@login_required
def crear_evaluacion(request):
    profesor = request.user

    # Filtrar solo los cursos que dicta este profesor
    cursos_del_profesor = Curso.objects.filter(profesor=profesor)

    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)

            # Verifica que el curso sea del profesor
            if evaluacion.curso in cursos_del_profesor:
                evaluacion.save()
                return redirect('panel_profesor')
            else:
                form.add_error('curso', 'No puedes crear evaluaciones para cursos que no dictas.')
    else:
        form = EvaluacionForm()
        # Limita los cursos al profesor
        form.fields['curso'].queryset = cursos_del_profesor

    return render(request, 'crear_evaluacion.html', {'form': form})