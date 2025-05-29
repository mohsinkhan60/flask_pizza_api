from flask import Flask
from flask_restx import Api
from api.config.config import config_dict

from api.orders.views import orders_namespace
from api.auth.views import auth_namespace

def create_app(config=config_dict['dev']):
   app = Flask(__name__)

   app.config.from_object(config)

   api = Api(app)
   api.add_namespace(orders_namespace)
   api.add_namespace(auth_namespace)

   return app