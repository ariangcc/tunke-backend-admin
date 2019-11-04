from app import db
from models.campaign import Campaign
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
import status

class CampaignResource(AuthRequiredResource):
	def get(self, id):
		try:
			campaign = Campaign.query.get_or_404(id)
			d = campaign.toJson()
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

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
