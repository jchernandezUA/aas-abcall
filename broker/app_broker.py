import time
from redis import Redis
from rq import Queue
from sender import process_command, handle_control, response_control

# Configuración de Redis con SSL/TLS (ajustar según tu caso)
redis_conn = Redis(
    host='redis',
    port=6379,
    ssl=True,
    ssl_certfile='/etc/broker/tls/broker-cert.pem',
    ssl_keyfile='/etc/broker/tls/llave.pem',
    ssl_ca_certs='/etc/broker/tls/ca-cert.pem',
    ssl_cert_reqs='required'
)

# Definir las colas
q_comandos = Queue('comandos', connection=redis_conn)
q_control = Queue('control', connection=redis_conn)
q_control_respuesta = Queue('control_respuesta', connection=redis_conn)

def main():
    while True:
        try:
            job_command = q_comandos.enqueue(process_command, {'command': 'start'})
            print(f"Command job enqueued with ID: {job_command.id}")

            job_control = q_control.enqueue(handle_control, {'control': 'sent'})
            print(f"Control job enqueued with ID: {job_control.id}")

            job_control_response = q_control_respuesta.enqueue(response_control, {'control_response': 'sent'})
            print(f"Response job enqueued with ID: {job_control_response.id}")

            # Esperar antes de volver a encolar trabajos
            time.sleep(5)

        except Exception as e:
            print(f"Error en el broker: {e}")

if __name__ == '__main__':
    main()
