from app import db
from models.loan import Loan
from models.client import Client
from models.salesRecord import SalesRecord
from models.account import Account
from models.campaign import Campaign
from models.currency import Currency
from models.prospectiveClient import ProspectiveClient
from models.bankAccount import BankAccount
from models.person import Person
from models.transaction import Transaction
from models.lead import Lead
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request, render_template
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
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class LoanListResource(AuthRequiredResource):
	def get(self):
		try:
			loans = Loan.query.all()
			d= []
			for loan in loans:
				e = {}
				e.update(loan.toJson())
				lead = Lead.query.get_or_404(e['idLead'])
				campaign = Campaign.query.get_or_404(lead.idCampaign)
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
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error': str(e)}
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
			commission = requestDict['commission']
			idCampaign = requestDict['idCampaign']

			client = Client.query.get_or_404(idClient)
			if client.activeLoans==1:
				response = {'error':' El cliente tiene un préstamo activo'}
				return response, status.HTTP_400_BAD_REQUEST 
			client.activeLoans = 1
			client.update()

			salesRecord = SalesRecord(origin='Ventanilla', requestDate=datetime.now(), idRecordStatus=3,active=1,idClient=idClient,idProduct=2)
			salesRecord.add(salesRecord)
			db.session.flush()

			lead = Lead(idClient=idClient,idCampaign=idCampaign,minimumLoan=0,maximumLoan=amount,active=0,minimumPeriod=6,maximumPeriod=totalShares,interestRate=interestRate)
			lead.add(lead)
			db.session.flush()

			#Prestamo con campaña para clientes sin campaña
			loan = Loan(totalShares=totalShares,amount=amount,interestRate=interestRate,idLead=lead.id,idClient=idClient,idSalesRecord=salesRecord.id,idShareType=idShareType,active=1,idAccount=idAccount,share=share,commission=commission)
			loan.add(loan)
			
			db.session.commit()
			
			regLoan = Loan.query.get(loan.id)
			d={}
			d['idLoan'] = regLoan.id
			d['totalShares'] = regLoan.totalShares
			d['amount'] = regLoan.amount
			d['interestRate'] = regLoan.interestRate
			d['idClient'] = regLoan.idClient
			d['idSalesRecord'] = regLoan.idSalesRecord
			d['idShareType'] = regLoan.idShareType
			d['active'] = regLoan.active

			return d, status.HTTP_201_CREATED

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

"""
class GenerateCalendarResource(Resource):
	def post(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST

			idLoan = requestDict['idLoan']
			
			loan = Loan.query.get_or_404(idLoan)
			idClient = loan.idClient
			client = Client.query.get_or_404(idClient)
			prospectiveClient = ProspectiveClient.query.get_or_404(client.id)
			email = prospectiveClient.email1
			shares = Shares.query.filter_by(idLoan=idLoan)
			shareArray = []
			for share in shares:
				shareArray.append(share.toJson())
			
			print('Rendered')
			rendered = render_template('calendar.html', shares=shareArray, currencySymbol=currencySymbol,totalAmortization=str(round(totalAmortization, 2)),totalInterest=str(round(totalInterest,2)),totalComission=str(round(totalComission,2)),totalShare=str(round(totalShare,2)))
			print('Pdfkit')
			pdf = pdfkit.from_string(rendered , False)
			print('PDF')
			msg.attach("Calendario.pdf","application/pdf",pdf)
			mail.send(msg)	
			return d, status.HTTP_201_CREATED
			
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
"""