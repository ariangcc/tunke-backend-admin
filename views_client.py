from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.client.openAccount import OpenAccountResource
from resources.client.dniValidation import DniValidationResource
from resources.admin.prospectiveClient import ProspectiveClientListResource
from resources.admin.parameterSettings import ParameterSettingsResource
from resources.client.securityQuestion import SecurityQuestionResource
from resources.client.sendToken import SendTokenResource
from resources.client.requestLoan import RequestLoanResource
from resources.admin.account import GetByClientResource
from resources.admin.lead import LeadResource

apiBp = Blueprint('api', __name__)
api = Api(apiBp)

api.add_resource(OpenAccountResource, '/openAccount/')
api.add_resource(DniValidationResource, '/dniValidation/')
api.add_resource(ProspectiveClientListResource, '/prospectiveClients/')
api.add_resource(SecurityQuestionResource, '/securityQuestions/')
api.add_resource(SendTokenResource, '/sendToken/')
api.add_resource(RequestLoanResource,'/requestLoan/')
api.add_resource(LeadResource,'/lead/<int:id>')
api.add_resource(ParameterSettingsResource, '/parameterSettings/')
api.add_resource(GetByClientResource, '/accounts/getByClient/')