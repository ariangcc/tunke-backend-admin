from app import db
from models.loan import Loan
from models.client import Client
from models.salesRecord import SalesRecord
from models.bankAccount import BankAccount
from models.account import Account
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import status

class RequestLoanResource(Resource):
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
			idCampaign = requestDict['idCampaign']
			idShareType = requestDict['idShareType']
			idAccount = requestDict['idAccount']

			#Minus en bank account
			bankAccount = BankAccount.query.get_or_404(1)
			bankAccount.balance = bankAccount.balance - amount
			bankAccount.update()

			#Plus in AccountClient
			account = Account.query.get_or_404(idAccount)
			account.balance = account.balance + amount
			account.update()
			
			#Update boolean in client
			client = Client.query.get_or_404(idClient)
			if client.activeLoans==1:
				response = {'error': 'El cliente tiene un préstamo activo'}
				return response, status.HTTP_400_BAD_REQUEST
			client.activeLoans = 1
			client.update()

			#Insert in salesRecord
			salesRecord = SalesRecord(origin='Origen default',requestDate=datetime.now(),idRecordStatus=1,
			active=1,idClient=idClient,idProduct=2)
			salesRecord.add(salesRecord)
			db.session.flush()

			#Insert in loan			
			loan = Loan(totalShares=totalShares,amount=amount,interestRate=interestRate,idCampaign=idCampaign,
			idClient=idClient,idSalesRecord=salesRecord.id,idShareType=idShareType,active=1)
			loan.add(loan)
			
			#Commit changes
			db.session.commit()

			regLoan = Loan.query.get(loan.id)
			d={}
			d['idLoan'] = regLoan.id
			d['totalShares'] = regLoan.totalShares
			d['amount'] = regLoan.amount
			d['interestRate'] = regLoan.interestRate
			d['idCampaign'] = regLoan.idCampaign
			d['idClient'] = regLoan.idClient
			d['idSalesRecord'] = regLoan.idSalesRecord
			d['idShareType'] = regLoan.idShareType
			d['active'] = regLoan.active 
			
			return d,status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST