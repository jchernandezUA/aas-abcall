# Dockerfile

# Usar una imagen base de Python
FROM python:3.8-slim

RUN mkdir /monitor

# Establecer el directorio de trabajo
WORKDIR /monitor

# Copiar los archivos de requirements y luego instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente al contenedor
ADD * /monitor/