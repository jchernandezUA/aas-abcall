# main.py
import redis
from rocketry import Rocketry
from rocketry.conds import every
import requests
import json


# Configurar cliente Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Crear la aplicación Rocketry
scheduler = Rocketry()

# Definir la función que revisa la cola de monitoreo
@scheduler.task(every('1 second'))  # Ejecutar cada segundo
def checar_cola_monitoreo():
    print('Entrando a checar_cola_monitoreo')  # Punto de depuración
    url_microservicio1 = "https://jsonplaceholder.typicode.com/posts"
     # URL del endpoint
    url_microservicio2 = "https://jsonplaceholder.typicode.com/invalid_endpoint"
    # Datos a enviar en el cuerpo de la solicitud
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }

    try:
        mensaje_recibido = redis_client.brpop('control', timeout=5)
        if mensaje_recibido:
            print("mensaje:::::", mensaje_recibido)
            try:
                requests.post(url_microservicio1, json=payload, timeout=5)
            except requests.exceptions.Timeout:
                mensaje_error = "El componente Llamada1 no respondió a la petición después de 5 segundos"
                print(mensaje_error)
                redis_client.lpush('control_respuesta', json.dumps({'component': 'LLamada1', 'estatus': 'false'}))

            try:
                requests.post(url_microservicio2, json=payload, timeout=5)
            except requests.exceptions.Timeout:
                mensaje_error = "El componente Llamada2 no respondió a la petición después de 10 segundos"
                print(mensaje_error)
                redis_client.lpush('control_respuesta', json.dumps({'component': 'LLamada2', 'estatus': 'false'}))
    except redis.RedisError as e:
        print(f"Error al conectar con Redis: {e}")


if __name__ == '__main__':
    # Ejecutar rocketry
    scheduler.run()