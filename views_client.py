from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.client.openAccount import OpenAccountResource
from resources.client.dniValidation import DniValidationResource
from resources.admin.prospectiveClient import ProspectiveClientListResource
from resources.client.securityQuestion import SecurityQuestionResource

apiBp = Blueprint('api', __name__)
api = Api(apiBp)

api.add_resource(OpenAccountResource, '/openAccount/')
api.add_resource(DniValidationResource, '/dniValidation/')
api.add_resource(ProspectiveClientListResource, '/prospectiveClients/')
api.add_resource(SecurityQuestionResource, '/securityQuestions/')