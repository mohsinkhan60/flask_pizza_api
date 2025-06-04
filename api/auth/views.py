from flask_restx import Namespace, Resource, fields
from flask import request
from api.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

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

login_model = auth_namespace.model(
    'Login',
    {
        'email': fields.String(required=True, description='Email address of the user'),
        'password': fields.String(required=True, description='Password of the user'),
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
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Log in an existing user.
        """
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user= User.query.filter_by(email=email).first()

        if user is not None and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        
@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Refresh the access token.
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, HTTPStatus.OK