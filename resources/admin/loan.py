from app import db
from models.loan import Loan
from models.client import Client
from models.salesRecord import SalesRecord
from models.account import Account
from models.campaign import Campaign
from models.currency import Currency
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import status

class LoanResource(AuthRequiredResource):
	def get(self,id):
		try:
			loan = Loan.query.get_or_404(id)
			d = loan.toJson()
			return d,status.HTTP_200_OK

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

			state = requestDict['state']

			loan = Loan.query.get_or_404(id)
			account = Account.query.get_or_404(loan.idAccount)
			client = Client.query.get_or_404(loan.idClient)
			salesRecord = SalesRecord.query.get_or_404(loan.idSalesRecord) 
			if state == 1:#aprobado
				salesRecord.idRecordStatus = 1
				salesRecord.requestDate = datetime.now()
				account.balance = account.balance + loan.amount
				client.activeLoans = 1
			elif state == 2:
				salesRecord.idRecordStatus = 2
				salesRecord.requestDate = datetime.now()
				client.activeLoans = 0

			salesRecord.update()
			client.update()
			account.update()
			db.session.commit()
			response = {'ok': 'Prestamo actualizado satisfactoriamente.'}
			return response, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class LoanListResource(AuthRequiredResource):
	def get(self):
		try:
			loans = Loan.query.all()
			d= []
			for loan in loans:
				e = {}
				e.update(loan.toJson())
				campaign = Campaign.query.get_or_404(e['idCampaign'])
				account = Account.query.get_or_404(e['idAccount'])
				client = Client.query.get_or_404(e['idClient'])
				prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
				person = Person.query.get_or_404(prospectiveClient.idPerson)
				salesRecord = SalesRecord.query.get_or_404(e['idSalesRecord'])
				salesRecord = salesRecord.toJson()
				e['campaignName'] = campaign.name
				e['accountNumber'] = account.accountNumber
				if account.idCurrency == 1:
					e['currency'] = 'Soles'
				elif account.idCurrency ==2:
					e['currency'] = 'Dólares'
				e['fullName'] = person.firstName + ' ' + person.fatherLastname
				e['documentNumber'] = person.documentNumber
				e['documentType'] = person.documentType
				e['requestDate'] = salesRecord['requestDate']
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
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST

			idClient = requestDict['idClient']
			totalShares = requestDict['totalShares']
			amount = requestDict['amount']
			interestRate = requestDict['interestRate']
			idShareType = requestDict['idShareType']
			idAccount = requestDict['idAccount']
			share = requestDict['share']

			client = Client.query.get_or_404(idClient)
			if client.activeLoans==1:
				response = {'error':' El cliente tiene un préstamo activo'}
				return response, status.HTTP_400_BAD_REQUEST 
			client.activeLoans = 1
			client.update()

			salesRecord = SalesRecord(origin='Origen default', requestDate=datetime.now(), idRecordStatus=3,active=1,idClient=idClient,idProduct=2)
			salesRecord.add(salesRecord)
			db.session.flush()
			
			#Prestamo con campaña para clientes sin campaña
			loan = Loan(totalShares=totalShares,amount=amount,interestRate=interestRate,idCampaign=2,idClient=idClient,idSalesRecord=salesRecord.id,idShareType=idShareType,active=1,idAccount=idAccount,share=share)
			loan.add(loan)

			db.session.commit()
			
			regLoan = Loan.query.get(loan.id)
			d={}
			d['idLoan'] = regLoan.id
			d['totalShares'] = regLoan.totalShares
			d['amount'] = regLoan.amount
			d['interestRate'] = regLoan.interestRate
			d['idCampaign'] = 2
			d['idClient'] = regLoan.idClient
			d['idSalesRecord'] = regLoan.idSalesRecord
			d['idShareType'] = regLoan.idShareType
			d['active'] = regLoan.active

			return d, status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

