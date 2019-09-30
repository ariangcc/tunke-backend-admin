from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.admin.user import UserListResource, UserResource
from resources.admin.authentication import LoginResource
from resources.admin.authentication import SignupResource
from resources.admin.account import AccountListResource, AccountResource
from resources.admin.transaction import TransactionListResource, TransactionResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(LoginResource, '/login')
api.add_resource(SignupResource, '/signup')
api.add_resource(AccountResource, '/accounts/<int:id>')
api.add_resource(AccountListResource, '/accounts/')
api.add_resource(TransactionResource, '/transactions/<int:id>')
api.add_resource(TransactionListResource, '/transactions/')