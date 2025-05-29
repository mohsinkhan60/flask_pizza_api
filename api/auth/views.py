from flask_restx import Namespace, Resource, fields

auth_namespace = Namespace('auth', description='Authentication related operations')

@auth_namespace.route('/')
class Home(Resource):
    def get(self):
        return {'message': 'Login endpoint'}, 200 