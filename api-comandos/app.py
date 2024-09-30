from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from redis import Redis
import json
import ssl

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

# Configurar conexión a Redis
#redis_client  = Redis(host='localhost', port=6379, db=0)


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
        #redis_client.lpush('commands', json.dumps(data))
        
        return {"message": "Comando encolado"}, 200

# Rutas para el API Comando
api.add_resource(ApiComando, '/comandos')

if __name__ == '__main__':

        # Crear contexto SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Cargar certificado y clave privada del servidor
    context.load_cert_chain(certfile='/etc/comandos/tls/api-comandos-cert.pem', keyfile='/etc/comandos/tls/llave.pem')

    # Cargar el certificado de la CA que firmó los certificados del cliente
    context.load_verify_locations(cafile='/etc/comandos/tls/ca-cert.pem')

    # Configurar Flask para que verifique el certificado del cliente
    context.verify_mode = ssl.CERT_REQUIRED

    # Correr la aplicación Flask en HTTPS y con autenticación mutua TLS (mTLS)
    app.run(debug=True, ssl_context=context, host='0.0.0.0', port=5003)

    #app.run(debug=True, port=5003)
