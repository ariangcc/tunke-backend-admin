from app import db
from datetime import datetime
from models.account import Account
from models.accountType import AccountType
from models.client import Client
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from models.currency import Currency
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
import status
from datetime import timedelta


class AccountResource(AuthRequiredResource):
	def get(self, id):
		try:
			account = Account.query.get_or_404(id)
			client = Client.query.get_or_404(account.idClient)
			prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
			person = Person.query.get_or_404(prospectiveClient.idPerson)
			currency = Currency.query.get_or_404(account.idCurrency)
			accountType = AccountType.query.get_or_404(account.idAccountType)
			d = {}
			d['firstName'] = person.firstName
			d['middleName'] = person.middleName
			d['fatherLastname'] = person.fatherLastname
			d['motherLastname'] = person.motherLastname
			d['active'] = account.active and client.active
			d.update(account.toJson())
			d.update(currency.toJson())
			d.update(accountType.toJson())
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
	
	def delete(self, id):
		try:
			account = Account.query.get_or_404(id)
			account.active = 0
			account.closingDate = datetime.now() - timedelta(hours=5)
			account.update()
			db.session.commit()
			resp = {'ok': 'Cuenta borrada satisfactoriamente.'}
			return resp, status.HTTP_204_NO_CONTENT
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class AccountListResource(AuthRequiredResource):
	def get(self):
		try:
			accounts = Account.query.all()
			d = {}
			d['accounts'] = []
			for account in accounts:
				client = Client.query.get_or_404(account.idClient)
				prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
				person = Person.query.get_or_404(prospectiveClient.idPerson)
				currency = Currency.query.get_or_404(account.idCurrency)
				accountType = AccountType.query.get_or_404(account.idAccountType)
				e = {}
				e['firstName'] = person.firstName
				e['middleName'] = person.middleName
				e['fatherLastname'] = person.fatherLastname
				e['motherLastname'] = person.motherLastname
				e['active'] = account.active and client.active
				e.update(account.toJson())
				e.update(currency.toJson())
				e.update(accountType.toJson())
				d['accounts'].append(e)
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class GetByClientResource(Resource):
	def post(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST
			
			idClient = requestDict['idClient']

			accounts = Account.query.filter_by(idClient=idClient)
			d = {}
			d['accounts'] = []
			for account in accounts:
				e = account.toJson()
				d['accounts'].append(e)
			
			return d, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class GetByNationality(Resource):
	def post(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST
			
			nationality = requestDict['nationality']

			#Obtener clientes por nacionalidad
			persons = Person.query.filter_by(nationality=nationality)
			prospectiveClients = []
			for person in persons:
				idPerson = person.id
				prospectiveClient = ProspectiveClient.query.filter_by(idPerson=idPerson).first()
				if prospectiveClient is not None:
					prospectiveClients.append(prospectiveClient.id)
			
			clients = []
			for idProspectiveClient in prospectiveClients:
				client = Client.query.filter_by(idProspectiveClient=idProspectiveClient).first()
				if client is not None:
					clients.append(client.id)
			
			d = {}
			d['accounts'] = []
			for idClient in clients:
				accounts = Account.query.filter_by(idClient=idClient)
				for account in accounts:
					d['accounts'].append(account.toJson())
			
			return d, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class GetByPeriod(Resource):
	def post(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST
			
			month, year = -1, -1
			year = int(requestDict['year'])
			if 'month' in requestDict:
				month = int(requestDict['month'])

			accounts = Account.query.all()
			ans = 0
			if month != -1: # Hay mes, separar por 4 semanas
				d = {}
				d['count'] = [0 for i in range(4)]
				for account in accounts:
					dateLst = [int(x) for x in account.openingDate.strftime('%d %m %Y').split()]
					dateDay, dateMonth, dateYear = dateLst[0], dateLst[1], dateLst[2]
					if dateMonth != month or dateYear != year:
						continue
					if dateDay <= 7:
						d['count'][0] += 1
					elif dateDay > 7 and dateDay <= 14:
						d['count'][1] += 1
					elif dateDay > 14 and dateDay <= 21:
						d['count'][2] += 1
					else:
						d['count'][3] += 1
				
				return d, status.HTTP_200_OK
					
			else: #No hay mes, separar por 12 meses
				d = {}
				d['count'] = [0 for i in range(12)]
				for account in accounts:
					dateLst = [int(x) for x in account.openingDate.strftime('%m %Y').split()]
					dateMonth, dateYear = dateLst[0], dateLst[1]
					d['count'][dateMonth - 1] += 1
				
				return d, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST