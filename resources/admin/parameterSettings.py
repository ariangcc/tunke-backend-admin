from app import db
from models.parameterSettings import ParameterSettings
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
import status

class ParameterSettingsResource(AuthRequiredResource):
	def get(self):
		try:
			parameterSettings = ParameterSettings.query.filter_by(id=1).first()
			d = parameterSettings.toJson()
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST