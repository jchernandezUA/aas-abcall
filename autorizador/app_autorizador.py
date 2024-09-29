from base import app, api, Resource, permission_required, create_token, jsonify, request, decode_token



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

if __name__ == '__main__':
    app.run(ssl_context=('/etc/autorizador/tls/autorizador-cert.pem', '/etc/autorizador/tls/llave.pem'), host='0.0.0.0', port=5005)

