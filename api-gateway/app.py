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
API_COMANDO_URL = "https://localhost:5003"
AUTH_SERVICE_URL = "https://localhost:5005"

api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

def check_permissions(request, data):
    ## valida permisos del usuario con el autorizador
    response_auth = requests.post(
        f"{AUTH_SERVICE_URL}/validate", 
        headers=request.headers,
        json=data, verify=False)
    response_auth.raise_for_status()

class ApiGateway(Resource):

    @jwt_required()
    def get(self, service_name, resource_name=''):
        url = self.parseUrl(service_name)
        if url is None:
            return {"error": "Servicio no encontrado"}, 404
        
        try:
            response = requests.get(
                f"{url}/{resource_name}",
                verify=False
            )
            check_permissions(request, {"method": "GET"})
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @jwt_required()
    def post(self, service_name, resource_name=''):
        url = self.parseUrl(service_name)
        if url is None:
            return {"error": "Servicio no encontrado"}, 404

        try:
            if resource_name:
                full_url = f"{url}/{resource_name}"
            else:
                full_url = url
            
            data = request.get_json()

            check_permissions(request, {"method": "POST"})

            #redirige la petición al microservicio
            response = requests.post(full_url, json=data, verify=False)
            response.raise_for_status()
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
        elif service_name == 'auth-service':
            return AUTH_SERVICE_URL
        else:
            return None

class LoginVista(Resource):
    def post(self):
        data = request.get_json()
        try:
            response = requests.post(f"{AUTH_SERVICE_URL}/login", json=data, verify=False)
            response.raise_for_status()  # Verificar si hay un error HTTP
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500


api.add_resource(ApiGateway, '/api/<string:service_name>/', '/api/<string:service_name>/<string:resource_name>')
api.add_resource(LoginVista, '/api/auth-service/login')

if __name__ == '__main__':
    app.run(ssl_context=('../nginx/tls/certificado.pem', '../nginx/tls/llave.pem'), host='0.0.0.0', port=6000)
