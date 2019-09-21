from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.user import UserListResource, UserResource
from resources.authentication import LoginResource
from resources.authentication import SignupResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(LoginResource, '/login')
api.add_resource(SignupResource, '/signup')