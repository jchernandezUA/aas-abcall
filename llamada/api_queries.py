import random
from base import app, api, Resource, Llamada, llamada_schema, redis_client, request
import json
import time

class LLamadaHealth(Resource):
    def get(self):
        try:
             # Obtener los parámetros de la solicitud GET y decodificar el JSON
            params = request.args.to_dict()

            # Convertir los parámetros JSON en un diccionario Python
            arrival_time = params.get('time')  
            message = params.get('message')

            # Obtener todas las llamadas desde la base de datos
            llamadas = Llamada.query.all()            
            # Serializar los datos de llamadas
            serialized_llamadas = llamada_schema.dump(llamadas, many=True)
             #Enviar a la cola de respuesta con el nombre nombre hora en que genero el tiempo el monitor y la hora de respuesta del servicio, estatus true
            redis_client.lpush('control_respuesta', json.dumps({'name': 'LLAMADAS', 'status': 'true', 'arrival_time': arrival_time, 'departure_time':time.time()}))
            # Retornar los datos serializados y un código de estado 200
            return serialized_llamadas, 200
        
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir
            print(f"Error al obtener llamadas: {e}")
            #Enviar a la cola de respuesta con el nombre nombre hora en que genero el tiempo el monitor y la hora de respuesta del servicio estatus false
            redis_client.lpush('control_respuesta', json.dumps({'name': 'LLAMADAS', 'status': 'false', 'arrival_time': arrival_time, 'departure_time':time.time()}))
            # Retornar un mensaje de error y un código de estado 500
            return {"message": "Error al obtener llamadas"}, 500
    
class LLamadaList(Resource):
    def get(self):
        return [{
            "id": "1000",
            "user": 10,
            "duration": "00:20:15"
        }]
    

api.add_resource(LLamadaHealth, '/api-queries/health')
api.add_resource(LLamadaList, '/llamadas')

if __name__ == '__main__':
    app.run(ssl_context=('../nginx/tls/certificado.pem', '../nginx/tls/llave.pem'), host='0.0.0.0', port=5001)



