# Usar una imagen base de Python
FROM python:3.8-slim

RUN mkdir /broker

# Instalar redis-tools para usar redis-cli
RUN apt-get update && apt-get install -y redis-tools

# Establecer el directorio de trabajo
WORKDIR /broker

# Copiar los archivos de requirements y luego instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente al contenedor
COPY . /broker/

# Exponer el puerto
EXPOSE 6379
