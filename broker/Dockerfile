# Dockerfile

# Usar una imagen base de Python
FROM python:3.8-slim

RUN mkdir /broker

# Establecer el directorio de trabajo
WORKDIR /broker

# Copiar los archivos de requirements y luego instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente al contenedor
ADD * /broker/

#exponiendo el puerto
EXPOSE 6379
