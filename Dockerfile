# Imagen base oficial de Python
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y fuerza el envío de logs a la salida estándar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# Crear carpeta para subida de archivos/imágenes si no existe
RUN mkdir -p app/static/uploads

# Exponer el puerto de Flask
EXPOSE 5000

# Comando para iniciar la aplicación con Gunicorn en producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]