from app import db
from models.campaign import Campaign
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
import status

class CampaignResource(AuthRequiredResource):
	def get(self,id):
		try:
			campaign = Campaign.query.get_or_404(id)
			d = campaign.toJson()
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

	def put(self,id):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error', 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST

			name = requestDict['name']
			month = requestDict['month']
			startDate = requestDict['startDate']
			endDate = requestDict['endDate']

			campaign = Campaign.query.get_or_404(id)

			campaign.name = name
			campaign.month = month
			campaign.startDate = startDate
			campaign.endDate = endDate

			campaign.update()
			db.session.commit()

			response = {'ok': 'Campaña actualizada correctamente'}
			return response, status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

	def delete(self,id):
		try:
			campaign = Campaign.query.get_or_404(id)
			campaign.active = 0
			campaign.update()

			db.session.commit()

			response = {'ok' : 'Campaña eliminada correctamente'}
			return response,status.HTTP_200_OK
			
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response,status.HTTP_400_BAD_REQUEST


class CampaignListResource(AuthRequiredResource):
	def get(self):
		try:
			campaigns = Campaign.query.all()
			d = []
			for campaign in campaigns:
				e = campaign.toJson()
				d.append(e)

			return d, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

			
	def post(self):
		requestDict = request.get_json()
		if not requestDict:
			response = {'error': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST

		try:
			name = requestDict['name']
			month = requestDict['month']
			startDate = requestDict['startDate']
			endDate = requestDict['endDate']
			idCurrency = requestDict['idCurrency']

			campaign = Campaign(name=name,month=month,startDate=startDate,endDate=endDate,idCurrency=idCurrency,active=1)
			campaign.add(campaign)
			db.session.commit()
			query = Campaign.query.get(campaign.id)
			result = query.toJson()
			return result, status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class CampaignChargeResource(AuthRequiredResource):
	def post(self):
		requestDict = request.get_json()
		if not requestDict:
			response = {'error' : 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		
		try:
			for camp in requestDict:
				campaign = Campaign(name=camp['name'],month=camp['month'],startDate=camp['startDate'],endDate=camp['endDate'],minimumLoan=camp['minimumLoan'],maximumLoan=camp['maximumLoan'],minimumPeriod=camp['minimumPeriod'],maximumPeriod=camp['maximumPeriod'],interestRate=camp['interestRate'],idCurrency=camp['idCurrency'],active=1)
				campaign.add(campaign)

			db.session.commit()
			response = {'ok' : 'Campañas añadidas correctamente'}
			return response, status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST
