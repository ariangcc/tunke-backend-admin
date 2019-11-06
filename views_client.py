from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.client.openAccount import OpenAccountResource
from resources.client.dniValidation import DniValidationResource
from resources.admin.prospectiveClient import ProspectiveClientListResource
from resources.client.securityQuestion import SecurityQuestionResource
from resources.client.sendToken import SendTokenResource
from resources.client.requestLoan import RequestLoanResource

apiBp = Blueprint('api', __name__)
api = Api(apiBp)

api.add_resource(OpenAccountResource, '/openAccount/')
api.add_resource(DniValidationResource, '/dniValidation/')
api.add_resource(ProspectiveClientListResource, '/prospectiveClients/')
api.add_resource(SecurityQuestionResource, '/securityQuestions/')
api.add_resource(SendTokenResource, '/sendToken/')
api.add_resource(RequestLoanResource,'/requestLoan/')