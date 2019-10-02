from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.client.openaccount import OpenAccountResource
from resources.client.dnivalidation import DniValidationResource
from resources.admin.prospectiveclient import ProspectiveClientListResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(OpenAccountResource, '/openaccount/')
api.add_resource(DniValidationResource, '/dnivalidation/')
api.add_resource(ProspectiveClientListResource, '/prospectiveclients/')