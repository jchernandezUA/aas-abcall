# main.py
import redis
from rocketry import Rocketry
from rocketry.conds import every
import json
import asyncio
import aiohttp


# Configurar cliente Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Lista de URLs de microservicios
MICROSERVICIOS = [
    'http://localhost:5000/api-queries/llamadas',
    #'http://localhost:5001/api-queries/llamadas2',
    # Añade más URLs de microservicios según sea necesario
]

# Crear la aplicación Rocketry asincrona
scheduler = Rocketry(execution="async")

# Definir la función que revisa la cola de monitoreo
@scheduler.task(every('1 second'))  # Ejecutar cada segundo
async def send_health_check():
    print('Entrando a send_health_check')  # Punto de depuración

    try:
        # Obtener el mensaje de la cola 'control'
        mensaje_recibido = redis_client.brpop('control', timeout=5)
        if mensaje_recibido:
            try:
                # Decodificar el mensaje recibido desde la cola
                mensaje = json.loads(mensaje_recibido[1].decode('utf-8'))
                print("mensaje recibido:::::", mensaje)

                # Enviar peticiones GET a todos los microservicios de forma asíncrona con los parámetros del mensaje
                await asyncio.gather(*[enviar_peticion_get(url, mensaje) for url in MICROSERVICIOS])

            except json.JSONDecodeError:
                print("Error al decodificar el mensaje JSON.")
    except redis.RedisError as e:
        print(f"Error al conectar con Redis: {e}")

# Función asíncrona para enviar peticiones GET a cada microservicio
async def enviar_peticion_get(url, parametros):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=parametros, timeout=5) as response:
                if response.status == 200:
                    print(f"Solicitud exitosa a {url}")
                    # No necesitas registrar aquí la respuesta, ya que el microservicio
                    # enviará su estado a la cola 'control_respuesta'
                else:
                    print(f"Error: Código de estado {response.status} para {url}")
        except aiohttp.ClientError as e:
            print(f"Error al conectar con el microservicio {url}: {e}")


if __name__ == '__main__':
    # Ejecutar rocketry
    scheduler.run()