from flask_restx import Namespace, Resource, fields

auth_namespace = Namespace('auth', description='Authentication related operations')

@auth_namespace.route('/')
class HomeAuth(Resource):
    def get(self):
        return {'message': 'Hellow Mohsin ! '}, 200 