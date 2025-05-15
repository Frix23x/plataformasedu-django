# views.py
# Este archivo contiene todas las vistas del proyecto (la lógica de las páginas).
# Cada función representa una página (HTML) que el usuario puede ver o interactuar.

from django.contrib import messages  # Sistema de mensajes (flash messages)
from django.contrib.auth import (  # Funciones de autenticación y login de Django
    authenticate, login)
from django.contrib.auth.decorators import \
    login_required  # Decorador para requerir login en una vista
from django.http import HttpResponse  # Para respuestas simples
from django.shortcuts import (  # render para mostrar HTML, redirect para redirecciones
    get_object_or_404, redirect, render)
from django.views.decorators.http import \
    require_POST  # Decorador para aceptar solo POST

from .forms import EvaluacionForm, RegistroForm  # Formularios personalizados
from .models import Evaluacion  # Modelos que se usan en las vistas
from .models import Curso, Inscripcion, Usuario


# 📝 Vista de registro de usuario
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirige a la página de login tras registrar
    else:
        form = RegistroForm()
    return render(request, "registro.html", {"form": form})


# 🔐 Vista de login con redirección automática según el rol del usuario
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            # Redirige según el rol del usuario
            if usuario.rol == "admin":
                return redirect("/admin/")
            elif usuario.rol == "profesor":
                return redirect("/panel-profesor/")
            else:
                return redirect("/panel-estudiante/")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "login.html")


# 👨‍🏫 Vista del panel del profesor
@login_required
def panel_profesor(request):
    if request.user.rol != 'profesor':
        return HttpsResponse("Solo los profores pueden acceder. Vete", status=403)
    profesor = request.user

    # Obtiene todos los cursos que dicta el profesor
    cursos = Curso.objects.filter(profesor=profesor)

    # Por cada curso, obtener la lista de estudiantes inscritos
    cursos_con_estudiantes = []
    for curso in cursos:
        estudiantes = Usuario.objects.filter(inscripcion__curso=curso)
        cursos_con_estudiantes.append((curso, estudiantes))

    return render(
        request,
        "panel_profesor.html",
        {"cursos_con_estudiantes": cursos_con_estudiantes},
    )


# 🎓 Vista del panel del estudiante
@login_required
def panel_estudiante(request):
    if request.user.rol != 'estudiante':
        return HttpResponse("Solo los estudiantes pueden acceder.", status=403)
    usuario = request.user

    # Cursos donde el estudiante ya está inscrito
    cursos_inscritos = Curso.objects.filter(inscripcion__estudiante=usuario)

    # Cursos que aún no ha tomado
    cursos_disponibles = Curso.objects.exclude(inscripcion__estudiante=usuario)

    return render(
        request,
        "panel_estudiante.html",
        {
            "cursos_disponibles": cursos_disponibles,
            "cursos_inscritos": cursos_inscritos,
        },
    )


# ➕ Vista para inscribirse a un curso (solo vía POST)
@login_required
@require_POST
def inscribirse(request, curso_id):
    curso = Curso.objects.get(id=curso_id)

    # Evita inscribirse dos veces al mismo curso
    ya_inscrito = Inscripcion.objects.filter(
        estudiante=request.user, curso=curso
    ).exists()

    if not ya_inscrito:
        Inscripcion.objects.create(estudiante=request.user, curso=curso)

    return redirect("panel_estudiante")


# 📋 Vista para que el estudiante vea sus evaluaciones
@login_required
def evaluaciones_estudiante(request):
    usuario = request.user

    # Encuentra todos los cursos donde está inscrito
    cursos_inscritos = Curso.objects.filter(inscripcion__estudiante=usuario)

    # Y luego encuentra las evaluaciones de esos cursos
    evaluaciones = Evaluacion.objects.filter(curso__in=cursos_inscritos).order_by(
        "fecha"
    )

    return render(
        request, "evaluaciones_estudiante.html", {"evaluaciones": evaluaciones}
    )


# 📝 Vista para que el profesor cree una evaluación
@login_required
def crear_evaluacion(request):
    # 🔐 Bloqueo directo si el usuario no es profesor
    if request.user.rol != 'profesor':
        return HttpResponse("Solo los profesores pueden crear evaluaciones. FUERA DE ACA", status=403)

    profesor = request.user
    cursos_del_profesor = Curso.objects.filter(profesor=profesor)

    if request.method == "POST":
        form = EvaluacionForm(request.POST, request.FILES, instance=evaluacion)
        if form.is_valid():
            messages.success(request, "✅ Evaluación creada exitosamente.")
            evaluacion = form.save(commit=False)

            if evaluacion.curso in cursos_del_profesor:
                evaluacion.save()
                return redirect("panel_profesor")
            else:
                form.add_error("curso", "No puedes crear evaluaciones para cursos que no dictas.")
    else:
        form = EvaluacionForm()
        form.fields["curso"].queryset = cursos_del_profesor

    return render(request, "crear_evaluacion.html", {"form": form})

# Vista para editar una evaluación
@login_required
def editar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)

    if request.user != evaluacion.curso.profesor:
        return HttpResponse("No tienes permiso para editar esta evaluacion. Fuera de aca", status=403)
    
    if 'eliminar_pdf' in request.POST:
        evaluacion.archivo_pdf.delete(save=True)
        messages.success(request, "🗑️ Archivo PDF eliminado exitosamente.")
        return redirect('editar_evaluacion', evaluacion_id=evaluacion.id)

    if request.method == "POST":
        form = EvaluacionForm(request.POST, request.FILES, instance=evaluacion)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cambios guardados correctamente.")
            return redirect("panel_profesor")
    else:
        form = EvaluacionForm(instance=evaluacion)

    return render(request, "editar_evaluacion.html", {"form": form})


# ! Eliminar una evaluacion
@login_required
@require_POST
def eliminar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)

    if request.user != evaluacion.curso.profesor:
        return HttpResponse("No tienes permiso para eliminar esta evaluacion. Fuera de aca", status=403)
    
    evaluacion.delete()
    return redirect("panel_profesor")
