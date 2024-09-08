# AAS-ABCALL - main

Prueba experimental relacionada con la materia de Arquitecturas Ágiles de Software

## Integrantes
* Jose Carlos Hernández
* Nelson Leonel Fonseca Ochoa
* Nicolas Esteban Garcia Valde
* Sergio Mena Zamora

## Instalación

Pre-requisitos:
* Tener instalado Docker
* Tener instalado docker-compose


Una vez que bajo el proyecto de GitHub proceder a ejecutar los contenedores en segundo plano y construir los mismos con el siguiente comando de docker-compose p:

```
docker-compose up -d --build
```

Esto para levantar los contenedores:
* aas-abcall-receptor
* aas-abcall-broker
* aas-abccall-monitor
* aas-abcall-llamadas

## Explicación breve de cada contenedor

* broker se encarga de la cola se mensajes (control, control_respuesta, comandos)
* monitoreo continuamente checando el estado de salud al estar generando eventos en la cola de control y monitoreando la cola control_respuesta
* receptor componente con la responsabilidad de estar monitoreando la cola de control y creando comunicación sincrona con los componentes de LLamadas
* llamadas principal se encarga de recibir los comandos o queries del elemento receptor y su funcion es ser el servicio principal
* llamadas redundante se encarga de recibir los comandos o queries del elemento receptor y su funcion es ser el servicio redundante, si falla el principal este entre a reemplazarlo.


