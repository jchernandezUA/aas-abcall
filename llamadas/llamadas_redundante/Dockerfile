# Dockerfile

# Usar una imagen base de Python
FROM python:3.8-slim

RUN mkdir /llamadas_redundante

# Establecer el directorio de trabajo
WORKDIR /llamadas_redundante

# Copiar los archivos de requirements y luego instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente al contenedor
ADD * /llamadas_redundante/
