# Dockerfile

# Usar una imagen base de Python
FROM python:3.8-slim

RUN mkdir /receptor

# Establecer el directorio de trabajo
WORKDIR /receptor

# Copiar los archivos de requirements y luego instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente al contenedor
ADD * /receptor/
