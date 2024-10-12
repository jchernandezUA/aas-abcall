from flask import Flask
from flask_restful import Api
from flask_cors import CORS




app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
cors = CORS(app)
api = Api(app)

