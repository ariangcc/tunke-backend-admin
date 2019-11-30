import datetime
from models.person import Person
from models.prospectiveClient import ProspectiveClient
from models.client import Client
from models.blacklist import Blacklist
from models.account import Account
from resources.admin.security import AuthRequiredResource
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource
from flask import request
from app import db
import status

class ProspectiveClientResource(Resource):
	def get(self, id):
		try:
			prospectiveClient = ProspectiveClient.query.get_or_404(id)
			d = prospectiveClient.toJson()
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class ProspectiveClientListResource(Resource):
	def get(self):
		try:
			prospectiveClients = ProspectiveClient.query.all()
			d = []
			for prospectiveClient in prospectiveClients:
				e = prospectiveClient.toJson()
				d.append(e)
			
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

	def post(self):
		requestDict = request.get_json()
		if not requestDict:
			response = {'error': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		
		idPerson = requestDict['idPerson']
		email1 = requestDict['email1']
		email2 = requestDict['email2']
		cellphone1 = requestDict['cellphone1']
		cellphone2 = requestDict['cellphone2']
		lastEnterDate = datetime.datetime.now()
		
		try:
			prospectiveClient = ProspectiveClient.query.filter_by(idPerson=idPerson).first()
			if not prospectiveClient:
				prospectiveClient = ProspectiveClient(idPerson=idPerson, email1=email1, email2=email2,
												  cellphone1=cellphone1, cellphone2=cellphone2,
												  lastEnterDate=lastEnterDate)
				prospectiveClient.enterCount = 1
				prospectiveClient.add(prospectiveClient)
				db.session.commit()
				query = ProspectiveClient.query.get(prospectiveClient.id)
				result = query.toJson()
				return result, status.HTTP_201_CREATED
			else:
				prospectiveClient.email1 = email1
				prospectiveClient.email2 = email2
				prospectiveClient.cellphone1 = cellphone1
				prospectiveClient.cellphone2 = cellphone2
				prospectiveClient.lastEnterDate = lastEnterDate
				prospectiveClient.enterCount += 1
				prospectiveClient.update()
				db.session.commit()
				query = ProspectiveClient.query.get(prospectiveClient.id)
				result = query.toJson()
				return result, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
			
