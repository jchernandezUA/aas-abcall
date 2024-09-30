from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_restful import Api, Resource
from datetime import datetime
from flask_cors import CORS
from faker import Faker
from datetime import datetime
import redis

cert_path = '/etc/llamada/tls/certificado.pem'
key_path = '/etc/llamada/tls/llave.pem'
ca_cert_path = '/etc/llamada/tls/ca-cert.pem'


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/llamadas.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///llamadas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
#redis_client = redis.Redis(host='redis', port=6379, db=0)
#redis_client = redis.Redis(host='redis', port=6379, db=0)

# Configuración del cliente Redis con SSL/TLS
redis_client = redis.StrictRedis(
    host='redis',  # Cambia esto al host de tu servidor Redis
    port=6379,  # Puerto por defecto de Redis
    ssl=True,
    ssl_certfile=cert_path,
    ssl_keyfile=key_path,
    ssl_ca_certs=ca_cert_path,
    ssl_cert_reqs='required'  # Asegura que se verifique el certificado del servidor
)



def cargar_datos_iniciales():
    try:
        #Borramos todo y creamos todo 
        db.drop_all() 
        db.create_all()
        data_factory = Faker()
        for i in range(10):
            llamada = Llamada(descripcion=data_factory.unique.name())
            db.session.add(llamada)
            db.session.commit()


    except Exception as e:
        print(f"Error al cargar los datos de carga iniciales {e}")
        db.session.rollback()


app.app_context().push()
db = SQLAlchemy()
db.init_app(app)

class Llamada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    descripcion = db.Column(db.String(length=120), nullable=False)

class LlamadaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Llamada
        fields = ("id", "fecha", "descripcion") 
        include_relationships = True,
        load_instance = True 

cargar_datos_iniciales()
cors = CORS(app)
api = Api(app)


llamada_schema = LlamadaSchema(many=True)


