from app import db
from models.loan import Loan
from models.client import Client
from models.salesRecord import SalesRecord
from models.bankAccount import BankAccount
from models.campaign import Campaign
from models.currency import Currency
from models.person import Person
from models.prospectiveClient import ProspectiveClient
from models.account import Account
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask_mail import Message
import status

class RequestLoanResource(Resource):
	def post(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST

			idClient = int(requestDict['idClient'])
			totalShares = int(requestDict['totalShares'])
			amount = float(requestDict['amount'])
			interestRate = float(requestDict['interestRate'])
			idCampaign = int(requestDict['idCampaign'])
			idShareType = int(requestDict['idShareType'])
			share = float(requestDict['share'])
			idAccount = int(requestDict['idAccount'])
			commission = float(requestDict['commission'])
			print(idClient, totalShares, amount, interestRate, idCampaign, idShareType, share, idAccount, commission)
			#Obteniendo campaign
			campaign = Campaign.query.get_or_404(idCampaign)

			#Minus en bank account
			bankAccount = BankAccount.query.get_or_404(campaign.idCurrency)
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
			idClient=idClient,idSalesRecord=salesRecord.id,idShareType=idShareType,active=1,idAccount=idAccount,share=share,commission=commission)
			loan.add(loan)
			
			#Commit changes
			print("hola")
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
			
			prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
			person = Person.query.get_or_404(prospectiveClient.idClient)
			currency = Currency.query.get_or_404(campaign.idCurrency)
			from mailing import mail
			msg = Message("Tunke - Prestamo otorgado exitosamente", sender="tunkestaff@gmail.com", recipients=[prospectiveClient.email1])
			msg.body = 'Hola'
			msg.html = render_template('loans.html', name=person.name + " " + person.fatherLastname, accountNumber=account.accountNumber, accountDetail='Cuenta Simple',
										currency=currency.currencyName, amount=amount)
			mail.send(msg)
			return d,status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST