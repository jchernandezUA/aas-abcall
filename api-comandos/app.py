from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from redis import Redis
import json

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

# Configurar conexión a Redis
redis_client  = Redis(host='localhost', port=6379, db=0)


# Inicialización de la API
api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

class ApiComando(Resource):

    def post(self):
        data = request.get_json()
        
        if not data:
            return {"error": "No se recibieron datos"}, 400
        
        # Convertir a JSON y agregar a la lista 'commands' en Redis
        redis_client.lpush('commands', json.dumps(data))
        
        return {"message": "Comando encolado"}, 200

# Rutas para el API Comando
api.add_resource(ApiComando, '/comandos')

if __name__ == '__main__':
    app.run(debug=True)