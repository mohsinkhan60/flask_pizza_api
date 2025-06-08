from flask import Flask
from flask_restx import Api
from api.config.config import config_dict
from api.orders.views import orders_namespace
from api.auth.views import auth_namespace
from api.utils import db
from api.models.orders import Order
from api.models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

def create_app(config=config_dict['dev']):
   app = Flask(__name__)

   app.config.from_object(config)

   db.init_app(app)

   jwt = JWTManager(app)

   migrate = Migrate(app, db)

   api = Api(app)

   api.add_namespace(orders_namespace)
   api.add_namespace(auth_namespace, path='/auth')

   @api.errorhandler(NotFound)
   def not_found(error):
       return {'error': 'Not found'}, 404
   
   @api.errorhandler(MethodNotAllowed)
   def method_not_allowed(error):
        return {'error': 'Method not allowed'}, 405

   @app.shell_context_processor
   def make_shell_context():
       return {
           'db': db,
           'User': User,
           'Order': Order
       }

   return app