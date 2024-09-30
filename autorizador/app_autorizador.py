from base import app, api, Resource, permission_required, create_token, jsonify, request, decode_token
from flask_jwt_extended import jwt_required, get_jwt



class VistaLogIn(Resource):
    def post(self):
        user_type = request.json.get('user_type')
        if not user_type:
            return {"message": "Missing user_type parameter"}, 400

        try:
            # Crear el token
            token = create_token(user_type)
            
            # Decodificar el token para obtener los claims
            decoded_token = decode_token(token)
            permissions = decoded_token.get('permissions', [])

            # Incluir permisos en la respuesta
            return {"access_token": token, "permissions": permissions}, 200
        except ValueError as e:
            return {"message": str(e)}, 400

api.add_resource(VistaLogIn, '/login')

class ValidateToken(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        method = data["method"]
        print(f"Headers recibidos: {request.headers}")
        print(f"JSON body recibido: {request.get_json()}")
        # Obtener los claims del token JWT
        claims = get_jwt()
        user_permissions = claims.get("permissions", [])

        print(f"Permisos en el token: {user_permissions}")

        # Verificar si el usuario tiene al menos uno de los permisos requeridos
        if method in user_permissions:
            return {"message": "Token and permissions are valid"}, 200
        else: 
            return {"message": "Permission denied"}, 401

# Añadir la ruta de validación al microservicio de autorización
api.add_resource(ValidateToken, '/validate')

if __name__ == '__main__':
    app.run(ssl_context=('../nginx/tls/autorizador-cert.pem', '../nginx/tls/llave.pem'), host='0.0.0.0', port=5005)


