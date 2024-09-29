FROM nginx:1.19.0-alpine
RUN rm /etc/nginx/conf.d/default.conf
# Configuracion para SSL/TLS
COPY ./docker/nginx/tls/certificado.pem /etc/nginx/tls/certificado.pem
COPY ./docker/nginx/tls/llave.pem /etc/nginx/tls/llave.pem