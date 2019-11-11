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

	def put(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error' : 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST

			maxTokenSends = requestDict['maxTokenSends']
			maxDiaryMovements = requestDict['maxDiaryMovements']
			legalAge = requestDict['legalAge']
			maxAccountsNumber = requestDict['maxAccountsNumber']
			commissionPercentage = requestDict['commissionPercentage']

			parameterSettings = ParameterSettings.query.filter_by(id=1).first()
			parameterSettings.maxTokenSends = maxTokenSends
			parameterSettings.maxDiaryMovements = maxDiaryMovements
			parameterSettings.legalAge = legalAge
			parameterSettings.maxAccountsNumber = maxAccountsNumber
			parameterSettings.commissionPercentage = commissionPercentage
			parameterSettings.update()

			db.session.commit()
			response = {'ok': 'Parámetros actualizados correctamente'}
			return response, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST
