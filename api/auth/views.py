from flask_restx import Namespace, Resource, fields
from flask import request
from api.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

auth_namespace = Namespace('auth', description='Authentication related operations')

signup_model = auth_namespace.model(
    'SignUp',
    {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='Username of the user'),
        'email': fields.String(required=True, description='Email address of the user'),
        'password': fields.String(required=True, description='Password of the user'),
    }
)

user_model = auth_namespace.model(
    'User',
    {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='Username of the user'),
        'email': fields.String(required=True, description='Email address of the user'),
        'password_hash': fields.String(required=True, description='Password of the user'),
        'is_staff': fields.Boolean(description='Is the user a staff member?'),
        'is_active': fields.Boolean(description='Is the user active?'),
    }
)

@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Sign up a new user.
        """
        data = request.get_json()

        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'))
        )

        new_user.save()
        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    
    def post(self):
        """
            Log in an existing user.
        """
        pass