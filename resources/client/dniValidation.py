from models.person import Person
from models.prospectiveClient import ProspectiveClient
from models.client import Client
from models.blacklist import Blacklist
from models.account import Account
from models.lead import Lead
from models.campaign import Campaign
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request, jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError
from flask_mail import Message
import status
from app import db
import requests, json

class DniValidationResource(Resource):
	def post(self):
		requestDict = request.get_json()
		if not requestDict:
			response = {'error': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST

		documentNumber = requestDict['documentNumber']
		try:
			blacklisted = (Blacklist.query.filter_by(documentNumber=documentNumber).first())
			d = {}
			if(blacklisted):
				d['type'] = 3
				return d, status.HTTP_200_OK
			else:
				person = (Person.query.filter_by(documentNumber=documentNumber).first())
				if not person:
					d['error'] = "La persona ingresada no existe en los registros"
					return d, status.HTTP_400_BAD_REQUEST

				prospectiveClient = (ProspectiveClient.query.filter_by(idPerson=person.id).first())

				if not prospectiveClient:
					d['type'] = 2 #Es no cliente, aun no es prospecto
					d.update(person.toJson())
					nationality = json.loads(requests.get('https://restcountries.eu/rest/v2/alpha/' + person.nationality).text)
					d['nationality'] = nationality['name']
					d['flag'] = nationality['flag']
					return d, status.HTTP_200_OK
				
				client = (Client.query.filter_by(idProspectiveClient=prospectiveClient.id).first())

				if not client:
					d['type'] = 2 #Es no cliente, ya es prospecto
					d.update(person.toJson())
					nationality = json.loads(requests.get('https://restcountries.eu/rest/v2/alpha/' + person.nationality).text)
					d['nationality'] = nationality['name']
					d['flag'] = nationality['flag']
					return d, status.HTTP_200_OK
				
				d['type'] = 1
				d.update(person.toJson())
				d.update(prospectiveClient.toJson())
				d.update(client.toJson())
				d['activeCampaigns'] = False
				leads = Lead.query.filter_by(idClient=client.id)
				for lead in leads:
					lead = lead.toJson()
					if(lead['active']):
						d['activeCampaigns'] = True
						campaign = Campaign.query.get_or_404(lead['idCampaign'])
						d['campaign'] = campaign.toJson()
						break

				nationality = json.loads(requests.get('https://restcountries.eu/rest/v2/alpha/' + person.nationality).text)
				d['nationality'] = nationality['name']
				d['flag'] = nationality['flag']
				return d, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
