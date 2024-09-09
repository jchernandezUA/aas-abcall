# AAS-ABCALL - main

Prueba experimental relacionada con la materia de Arquitecturas Ágiles de Software

## Integrantes
* Jose Carlos Hernández
* Nelson Leonel Fonseca Ochoa
* Nicolas Esteban Garcia Valde
* Sergio Mena Zamora

## Instalación

Pre-requisitos:
* Pyhton 3.11.5
* Virtual environment activado

Una vez que bajo el proyecto de GitHub proceder a ejecutar los siguientes comandos

```
pip install -r broker/requirements.txt
pip install -r llamada/requirements.txt
pip install -r llamada2/requirements.txt
pip install -r monitor/requirements.txt
pip install -r receptor/requirements.txt
```

## Explicación breve de cada contenedor

* broker se encarga de la cola se mensajes (control, control_respuesta, comandos)
* monitoreo continuamente checando el estado de salud al estar generando eventos en la cola de control y monitoreando la cola control_respuesta
* receptor componente con la responsabilidad de estar monitoreando la cola de control y creando comunicación sincrona con los componentes de LLamadas
* llamadas: Micro servicio de llamadas principal
* llamadas2: Micro servicio de llamdas redundante


## Ejecución

Para ejecutar el ejemplo se deben abrir 5 consolas diferentes y correr los siguientes comandos:

consola 2

```
python receptor/app_receptor.py
```

consola 2
```
python llamada/api_queries.py
```

consola 3

```
python llamada2/api_queries.py
```

consola 4

```
cd monitor
celery -A app_monitor beat
```

consola 5

```
cd monitor
celery -A app_monitor worker
```


Una vez corriendo estos comandos podrá notar como es que en el worker se van generando eventos en las colas de control y se están leyendo los mensajes de respuesta, así como los microservicios están respondendo estos mensajes de control.




