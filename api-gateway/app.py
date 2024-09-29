from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required

import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

# URLs de los microservicios corregidas
MICRO_LLAMADAS_URL = "http://localhost:5001"
MICRO_CHATBOT_URL = "http://localhost:5002"

api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

class ApiGateway(Resource):

    def get(self, service_name, resource_name=''):
        url = self.parseUrl(service_name)
        if url is None:
            return {"error": "Servicio no encontrado"}, 404

        try:
            response = requests.get(f"{url}/{resource_name}")
            response.raise_for_status()  # Verificar si hay un error HTTP
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    def post(self, service_name, resource_name=''):
        url = self.parseUrl(service_name)
        if url is None:
            return {"error": "Servicio no encontrado"}, 404
        data = requests.get_json()  # Datos del comando en JSON
        try:
            response = requests.post(f"{url}/{resource_name}", json=data)
            response.raise_for_status()  # Verificar si hay un error HTTP
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    def parseUrl(self, service_name):
        if service_name == 'llamadas-service':
            return MICRO_LLAMADAS_URL
        elif service_name == 'chatbot-service':
            return MICRO_CHATBOT_URL
        else:
            return None

api.add_resource(ApiGateway, '/api/<string:service_name>/', '/api/<string:service_name>/<string:resource_name>')
