from redis import Redis
from rq import Queue
from sender import process_command, handle_control, response_control


#Config de redis
redis_conn = Redis(host='redis', port=6379, db=0)
# Definir las colas
q_comandos = Queue('comandos', connection=redis_conn)
q_control = Queue('control', connection=redis_conn)
q_control_respuesta = Queue('control_respuesta', connection=redis_conn)


if __name__ == '__main__':
    job_command = q_comandos.enqueue(process_command, {'command': 'start'})
    print(f"Command job enqueued with ID: {job_command.id}")
    job_control = q_control.enqueue(handle_control, {'control': 'sent'})
    print(f"Control job enqueued with ID: {job_control.id}")
    job_control_response = q_control_respuesta.enqueue(response_control, {'control_response': 'sent'})
    print(f"Response job enqueued with ID: {job_control_response.id}")