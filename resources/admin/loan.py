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
from models.share import Share
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request, render_template
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from flask_mail import Message
import status
import pdfkit

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
				e['idRecordStatus'] =salesRecord['idRecordStatus']
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

			idClient = int(requestDict['idClient'])
			totalShares = int(requestDict['totalShares'])
			amount = float(requestDict['amount'])
			interestRate = float(requestDict['interestRate'])
			idShareType = int(requestDict['idShareType'])
			idAccount = int(requestDict['idAccount'])
			share = float(requestDict['share'])
			commission = float(requestDict['commission'])
			idCampaign = int(requestDict['idCampaign'])

			client = Client.query.get_or_404(idClient)
			if client.activeLoans==1:
				response = {'error':' El cliente tiene un préstamo activo'}
				return response, status.HTTP_400_BAD_REQUEST 
			client.activeLoans = 1
			client.update()

			today = datetime.now() - timedelta(hours=5)
			tea = interestRate
			tem = (((1 + (tea/100)) ** (1/12))-1)
			month = today.month			
			countExtraMonths = 0
			numberExtra = 0
			auxDate = today
			for i in range(totalShares):
				auxDate = auxDate + timedelta(days=30)
				monthAuxDate = auxDate.month
				if(monthAuxDate==7 or monthAuxDate==12):
					countExtraMonths+=1

			if(idShareType==2):
				numberExtra = countExtraMonths

			shareBase = round(	(amount * ( (1+tem) ** (totalShares + numberExtra) ) * tem) / ( ((1+tem) ** (totalShares + numberExtra)) - 1 ), 2)
			initialDebt = amount
			day = today
			totalAmortization = 0
			totalInterest = 0
			totalCommission = commission * totalShares
			totalShare = 0
			

			salesRecord = SalesRecord(origin='Ventanilla', requestDate=today, idRecordStatus=3,active=1,idClient=idClient,idProduct=2)
			salesRecord.add(salesRecord)
			db.session.flush()

			lead = Lead(idClient=idClient,idCampaign=idCampaign,minimumLoan=0,maximumLoan=amount,active=0,minimumPeriod=6,maximumPeriod=totalShares,interestRate=interestRate)
			lead.add(lead)
			db.session.flush()

			#Prestamo con campaña para clientes sin campaña
			loan = Loan(totalShares=totalShares,amount=amount,interestRate=interestRate,idLead=lead.id,idClient=idClient,idSalesRecord=salesRecord.id,idShareType=idShareType,active=1,idAccount=idAccount,share=share,commission=commission)
			loan.add(loan)
			db.session.flush()

			#Insert in shares
			for i in range(totalShares):
				auxShareBase = shareBase
				interest = round(initialDebt * tem,2)
				day = day + timedelta(days=30)
				if(idShareType == 2):
					if(day.month==7 or day.month==12):
						auxShareBase = round(shareBase*2,2)
				amortization = auxShareBase - interest
				if(i == totalShares-1):
					amortization = initialDebt
				feeAmount = amortization + commission + interest
				totalAmortization+=amortization
				totalInterest+=interest
				totalShare+=feeAmount
				share = Share(initialBalance=initialDebt,amortization=amortization,interest=interest,commission=commission,feeAmount=feeAmount,dueDate=day,idLoan=loan.id,shareNumber=i+1)
				share.add(share)
				initialDebt = initialDebt - amortization

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
			print(e)
			return response, status.HTTP_400_BAD_REQUEST


class GenerateCalendarResource(AuthRequiredResource):
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
			shares = Share.query.filter_by(idLoan=idLoan)
			shareArray = []
			totalAmortization, totalShare, totalInterest, totalComission = 0.0,0.0,0.0,0.0
			for share in shares:
				totalAmortization += share.amortization 
				totalShare += share.feeAmount
				totalInterest += share.interest
				totalComission += share.commission
				shareArray.append(share.toJson())
			lead = Lead.query.get_or_404(loan.idLead)
			campaign = Campaign.query.get_or_404(lead.idCampaign)
			currency = Currency.query.get_or_404(campaign.idCurrency)
			currencySymbol = currency.currencySymbol
			from mailing import mail
			msg = Message("Tunke - Calendario de pagos", sender="tunkestaff@gmail.com", recipients=[prospectiveClient.email1])
			msg.body = 'Calendario de pagos de tu prestamo!'
			print('Rendered')
			rendered = render_template('calendar.html', shares=shareArray, currencySymbol=currencySymbol,totalAmortization=str(round(totalAmortization, 2)),totalInterest=str(round(totalInterest,2)),totalComission=str(round(totalComission,2)),totalShare=str(round(totalShare,2)))
			print('Pdfkit')
			pdf = pdfkit.from_string(rendered , False)
			print('PDF')
			msg.attach("Calendario.pdf","application/pdf",pdf)
			mail.send(msg)
			d = {'ok': 'Calendario enviado correctamente'}
			return d, status.HTTP_201_CREATED
			
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

		except Exception as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
