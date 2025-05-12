# 📁 settings.py
# Este archivo configura todo el comportamiento del proyecto Django:
# bases de datos, apps instaladas, rutas, lenguaje, seguridad, etc.

from pathlib import Path

# Ruta base del proyecto (donde se encuentra manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Clave secreta para seguridad interna de Django (debe mantenerse secreta en producción)
SECRET_KEY = 'django-insecure-secret'

# 🔍 Si está en True, se muestran errores detallados en el navegador. Solo usar en desarrollo.
DEBUG = True

# 🌐 Lista de dominios que pueden acceder al sitio. Vacío en desarrollo.
ALLOWED_HOSTS = []

# 📦 Aplicaciones instaladas en este proyecto
INSTALLED_APPS = [
    'django.contrib.admin',           # Panel de administración de Django
    'django.contrib.auth',            # Sistema de autenticación (usuarios, contraseñas)
    'django.contrib.contenttypes',    # Tipos de contenido genéricos
    'django.contrib.sessions',        # Manejo de sesiones (cookies, login)
    'django.contrib.messages',        # Sistema de mensajes (flash messages)
    'django.contrib.staticfiles',     # Manejo de archivos estáticos (CSS, JS, imágenes)
    'usuarios',                       # Tu propia app personalizada llamada "usuarios"
]

# 🧱 Middleware: procesos que se ejecutan en cada request/response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Seguridad básica
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manejo de sesiones
    'django.middleware.common.CommonMiddleware',  # Funciones comunes para todos los requests
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Añade user al request
    'django.contrib.messages.middleware.MessageMiddleware',  # Permite usar mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protección contra clickjacking
]

# 🌐 Archivo que maneja las rutas principales del proyecto
ROOT_URLCONF = 'cursos_project.urls'

# 🧩 Configuración del sistema de plantillas HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de plantillas por defecto
        'DIRS': [],  # Aquí podrías agregar rutas de plantillas personalizadas (como 'templates/')
        'APP_DIRS': True,  # Activa auto-búsqueda de plantillas dentro de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Añade variable debug al contexto
                'django.template.context_processors.request',  # Añade el objeto request en templates
                'django.contrib.auth.context_processors.auth',  # Añade el usuario actual al contexto
                'django.contrib.messages.context_processors.messages',  # Añade mensajes al contexto
            ],
        },
    },
]

# 🧪 Especifica qué aplicación se usará para ejecutar en servidores (como Gunicorn)
WSGI_APPLICATION = 'cursos_project.wsgi.application'

# 🛢️ Configuración de la base de datos (en este caso MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Tipo de base de datos
        'NAME': 'cursos_db',                  # Nombre de la base de datos
        'USER': 'user',                       # Usuario
        'PASSWORD': 'userpass',               # Contraseña
        'HOST': 'db',                         # Nombre del host (puede ser 'localhost' o 'db' en Docker)
        'PORT': '3306',                       # Puerto por defecto de MySQL
    }
}

# 🔒 Validadores de contraseñas (puedes activarlos para mayor seguridad)
AUTH_PASSWORD_VALIDATORS = []

# 🌍 Configuración regional
LANGUAGE_CODE = 'es-pe'  # Idioma por defecto del proyecto (español de Perú)
TIME_ZONE = 'America/Lima'  # Zona horaria
USE_I18N = True  # Habilita internacionalización
USE_TZ = True    # Usa fechas y horas con zona horaria

# 🖼️ Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'  # URL base para archivos estáticos

# 📂 Ruta donde se ubica la carpeta de archivos estáticos en desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 🧑‍💻 Modelo de usuario personalizado
AUTH_USER_MODEL = 'usuarios.Usuario'

# 📦 En producción, se usará esta carpeta para recolectar todos los archivos estáticos (con collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'
