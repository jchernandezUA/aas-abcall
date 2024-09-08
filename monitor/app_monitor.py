from celery import Celery
import time
import json
from redis import Redis
import random


app = Celery('monitor', broker='redis://redis:6379/0')

app.conf.beat_schedule = {
    'health_check': {
        'task': 'monitor.send_control_health_check',
        'schedule': 2.0
    },

    'control_check': {
        'task': 'monitor.control_check',
        'schedule': 2.0
    },

    'componente': {
        'task': 'monitor.componente_llamadas',
        'schedule': 2.0
    }
}

app.conf.timezone = 'UTC'

redis_client = Redis(host='redis', port=6379, db=0)

# mensaje de control {'message':'health_check' , 'time': time.time()}
# mensaje de respuesta {'component': 'LLamada1', 'status': 'false', 'arrival_time': mensaje_control.time, 'departure_time':time.time()}

COMPONENTS = ['LLAMADAS']
QUEUE_CONTROL = 'control'
QUEUE_RESPONSE = 'control_respuesta'

@app.task
def send_control_health_check():
     for _ in range(len(COMPONENTS)):
        health_check_event = {'message':'health_check' , 'time': time.time()}
        redis_client.lpush(QUEUE_CONTROL, json.dumps(health_check_event))        
        log_message('control check {}'.format(time.time()))



@app.task
def control_check():

    ## DELAY DE 3 SEGUNDOS  
    if control_check.request.retries == 0:
        time.sleep(5)

    messages = redis_client.lrange(QUEUE_RESPONSE, 0,-1)
    
    list_components = COMPONENTS
    
    print(messages)
    for _ in range(len((messages))):
        element = redis_client.brpop(QUEUE_RESPONSE, timeout=1)
        if element:
            message = json.loads(element[1].decode('utf-8'))
            if message['name'] in list_components:
                if message['status'] == 'true':
                    list_components.remove(message['name'])
                    log_message('{} working OK'.format(message['name']))

        else:
            log_message('check connection redis')
    
    for remaining_element in list_components:
        send_notification(remaining_element)
    
    redis_client.delete(QUEUE_RESPONSE)

def send_notification(name):
    log_message('NOTIFICATION ALERT {}'.format(name))

@app.task
def componente_llamadas():
    if random.choice([True, False]):  
        log_message('COMPONENT RESPONDING')
        print(componente_llamadas.request.retries % 3)
        response = redis_client.brpop(QUEUE_CONTROL, timeout=1)
        if response:
            mensaje_decodificado = response[1].decode('utf-8')  
            print(mensaje_decodificado)
            request = json.loads(mensaje_decodificado)   
            print(request)
            response = json.dumps({'name': 'LLAMADAS', 'status': 'true', 'arrival_time': request['time'], 'departure_time':time.time()})  
            redis_client.lpush(QUEUE_RESPONSE, response)
        else:
            print('!!!!!')
            print('mensaje de control no recibido')
    else:
        log_message('SIMULATE NOT RESPONDING')
        

def log_message(message):
    print('\n*****************\n    {}    \n************************'.format(message))