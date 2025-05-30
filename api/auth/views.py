from flask_restx import Namespace, Resource, fields

auth_namespace = Namespace('auth', description='Authentication related operations')

@auth_namespace.route('/signup')
class SignUp(Resource):

    def post(self):
        """
            Sign up a new user.
        """
        pass


@auth_namespace.route('/login')
class Login(Resource):
    
    def post(self):
        """
            Log in an existing user.
        """
        pass