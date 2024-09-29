from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

MICRO_CORREO_URL = "http://localhost:5003"
MICRO_CHATBOT_URL = "http://localhost:5002"
MICRO_NOTIFICACIONES_URL = "http://localhost:5004"

api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

class ApiComando(Resource):

    @jwt_required()
    def post(self, service_name):
        url = self.parseUrl(service_name)
        if url is None:
            return {"error": "Servicio no encontrado"}, 404

        data = request.get_json()  
        try:
            response = requests.post(f"{url}/comando", json=data)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    def parseUrl(self, service_name):
        if service_name == 'correo-service':
            return MICRO_CORREO_URL
        elif service_name == 'chatbot-service':
            return MICRO_CHATBOT_URL
        elif service_name == 'notificaciones-service':
            return MICRO_NOTIFICACIONES_URL
        else:
            return None

api.add_resource(ApiComando, '/comando/<string:service_name>')

if __name__ == '__main__':
    app.run(debug=True)