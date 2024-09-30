from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required

import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

# URLs de los microservicios corregidas
MICRO_LLAMADAS_URL = "https://localhost:5001"
MICRO_CHATBOT_URL = "http://localhost:5002"
API_COMANDO_URL = "http://localhost:5003"
AUTH_SERVICE_URL = "http://localhost:5005"

api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

def check_permissions(token, required_permissions):
    try:
        headers = {
            "Authorization": f"{token}",
            "Content-Type": "application/json"  
        }
        data = {"permissions": required_permissions}

        print(f"Enviando permisos: {data}")  
        print(f"headers: {headers}")  

        response = requests.post(f"{AUTH_SERVICE_URL}/validate", headers=headers, json=data)
        response.raise_for_status()

        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error verificando permisos: {e}")
        return False

class ApiGateway(Resource):

    def get(self, service_name, resource_name=''):
        url = self.parseUrl(service_name)
        if url is None:
            return {"error": "Servicio no encontrado"}, 404
        
        # Obtener el token de la cabecera Authorization
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return {"error": "Falta el token JWT o no está en formato Bearer"}, 401

        # Validar el token y los permisos
        if not check_permissions(token, ["GET"]):
            return {"error": "Acceso denegado: Permisos insuficientes"}, 403
        
        try:
            
            response = requests.get(
                f"{url}/{resource_name}",
                verify=False
            )
            response.raise_for_status()  # Verificar si hay un error HTTP
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    def post(self, service_name, resource_name=''):
        url = self.parseUrl(service_name)
        if url is None:
            return {"error": "Servicio no encontrado"}, 404
        # Obtener el token de la cabecera Authorization
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "Falta el token JWT en la cabecera"}, 401

        # Validar el token y los permisos
        if not check_permissions(token, ["POST"]):
            return {"error": "Acceso denegado: Permisos insuficientes"}, 403       
        data = request.get_json()
        if not data:
            return {"error": "No se recibieron datos"}, 400
        try:
            if resource_name:
                full_url = f"{url}/{resource_name}"
            else:
                full_url = url
            
            response = requests.post(full_url, json=data)
            response.raise_for_status()  # Verificar si hay un error HTTP
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    def parseUrl(self, service_name):
        if service_name == 'llamadas-service':
            return MICRO_LLAMADAS_URL
        elif service_name == 'chatbot-service':
            return MICRO_CHATBOT_URL
        elif service_name == 'comandos-service':
            return API_COMANDO_URL
        else:
            return None

api.add_resource(ApiGateway, '/api/<string:service_name>/', '/api/<string:service_name>/<string:resource_name>')