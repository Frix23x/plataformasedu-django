FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && apt-get clean

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
