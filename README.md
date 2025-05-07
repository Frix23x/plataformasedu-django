# 📚 Plataforma Educativa - Django + Docker

Este es un proyecto de prueba desarrollado con **Python**, **Django**, **MySQL** y **Docker**, que simula una plataforma educativa con usuarios tipo **estudiante**, **profesor** y **administrador**.

## 🚀 Características

- Registro y login de usuarios con roles.
- Panel de estudiante:
  - Visualiza cursos disponibles e inscritos.
  - Se inscribe en cursos.
  - Visualiza evaluaciones asignadas.
- Panel de profesor:
  - Visualiza cursos que dicta.
  - Lista de estudiantes inscritos.
  - Crea evaluaciones para sus cursos.
- Navegación amigable y botones para cerrar sesión.

## ⚙️ Tecnologías

- Django 4.2
- Python 3.11
- MySQL 8
- Docker + Docker Compose
- HTML + CSS básico

## 🛠️ Instrucciones rápidas (modo Docker)

# Construir contenedores
docker-compose build

# Levantar proyecto
docker-compose up

/app
  └── usuarios/
      ├── models.py
      ├── views.py
      ├── templates/
      └── ...

## Estado actual

Proyecto en desarrollo con fines educativos. No orientado aún a producción.

## Autor

Desarrollado por [Santiago(Frix23x)](https://github.com/Frix23x) como práctica personal con Django, Docker y Git.

```bash