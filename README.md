# AAS-ABCALL - main

Prueba experimental relacionada con la materia de Arquitecturas Ágiles de Software

## Integrantes
Jose Carlos Hernández
Nelson Leonel Fonseca Ochoa
Nicolas
Sergio Mena Zamora

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
* llamadas pendiente


