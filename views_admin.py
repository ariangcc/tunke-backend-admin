from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.admin.user import UserListResource, UserResource
from resources.admin.authentication import LoginResource
from resources.admin.authentication import SignupResource
from resources.admin.person import PersonListResource, PersonResource, PersonDocumentResource
from resources.admin.client import ClientListResource, ClientResource
from resources.admin.account import AccountListResource, AccountResource 
from resources.admin.authentication import VerifyEmailResource
from resources.client.dniValidation import DniValidationResource

apiBp = Blueprint('api', __name__)
api = Api(apiBp)

api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(PersonResource, '/persons/<int:id>')
api.add_resource(PersonListResource, '/persons/')
api.add_resource(ClientResource, '/clients/<int:id>')
api.add_resource(ClientListResource, '/clients/')
api.add_resource(AccountResource, '/accounts/<int:id>')
api.add_resource(AccountListResource, '/accounts/')
api.add_resource(VerifyEmailResource, '/verifyEmail/')
api.add_resource(PersonDocumentResource, '/persons/getByDocument/')
api.add_resource(DniValidationResource, '/dniValidation/')
