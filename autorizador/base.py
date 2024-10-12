from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, decode_token
from flask_cors import CORS
from datetime import timedelta, datetime

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# Función para crear un token con permisos
def create_token(user_type):
    if user_type == "read_only":
        permissions = ["GET"]
    elif user_type == "read_write":
        permissions = ["GET", "POST"]
    else:
        raise ValueError("Invalid user type")

    # Crear el token con los permisos en sus claims
    token = create_access_token(identity=user_type, additional_claims={"permissions": permissions})
    return token

# Decorador para verificar permisos
def permission_required(required_permissions):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            # Obtener los claims del token
            claims = get_jwt()
            user_permissions = claims.get("permissions", [])

            # Verificar si el usuario tiene los permisos requeridos
            if not any(perm in user_permissions for perm in required_permissions):
                return jsonify({"message": "Permission denied"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper

app.app_context().push()

cors = CORS(app)
api = Api(app)

