from app import db
from models.loan import Loan
from models.lead import Lead
from models.client import Client
from models.salesRecord import SalesRecord
from models.bankAccount import BankAccount
from models.campaign import Campaign
from models.currency import Currency
from models.person import Person
from models.prospectiveClient import ProspectiveClient
from models.account import Account
from models.transaction import Transaction
from models.share import Share
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from flask import request, render_template
from flask_mail import Message
import logging
import status
import pdfkit

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
			idLead = int(requestDict['idLead'])
			idShareType = int(requestDict['idShareType'])
			share = float(requestDict['share'])
			idAccount = int(requestDict['idAccount'])
			commission = float(requestDict['commission'])

			#Update boolean in client
			client = Client.query.get_or_404(idClient)
			if client.activeLoans==1:
				response = {'error': 'El cliente tiene un préstamo activo'}
				return response, status.HTTP_400_BAD_REQUEST
			client.activeLoans = 0 # Esto deberia ser 0 (Soli)
			client.update()
			today = datetime.now() - timedelta(hours=5)

			#Calculo de tea y tem
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
			pot = totalShares + numberExtra
			auxTem = tem + 1
			shareBase = round(	(amount * ( (1+tem) ** (totalShares + numberExtra) ) * tem) / ( ((1+tem) ** (totalShares + numberExtra)) - 1 ), 2)
			initialDebt = amount
			day = today
			totalAmortization = 0
			totalInterest = 0
			totalCommission = commission * totalShares
			totalShare = 0
				
			today = datetime.now() - timedelta(hours=5)
			day = today

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

			#Insert in salesRecord
			salesRecord = SalesRecord(origin='Web',requestDate=datetime.now() - timedelta(hours=5),idRecordStatus=1,
			active=1,idClient=idClient,idProduct=2)
			salesRecord.add(salesRecord)
			db.session.flush()

			#Insert in loan		
			loan = Loan(totalShares=totalShares,amount=amount,interestRate=interestRate,idLead=idLead,
			idClient=idClient,idSalesRecord=salesRecord.id,idShareType=idShareType,active=1,idAccount=idAccount,share=share,commission=commission)
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

			#Insert in transaction
			transaction = Transaction(datetime=today,amount=amount,idAccount=idAccount,idBankAccount=campaign.idCurrency,active=1)
			transaction.add(transaction)

			lead = Lead.query.get_or_404(idLead)
			lead.active = 0
			lead.update()
			
			#Commit changes
			db.session.commit()

			regLoan = Loan.query.get(loan.id)
			d={}
			d['idLoan'] = str(regLoan.id)
			d['totalShares'] = str(regLoan.totalShares)
			d['amount'] = str(regLoan.amount)
			d['interestRate'] = str(regLoan.interestRate)
			d['idClient'] = str(regLoan.idClient)
			d['idSalesRecord'] = str(regLoan.idSalesRecord)
			d['idShareType'] = str(regLoan.idShareType)
			d['active'] = str(regLoan.active)
			prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
			person = Person.query.get_or_404(prospectiveClient.idPerson)
			currency = Currency.query.get_or_404(campaign.idCurrency)
			sharesA = Share.query.filter_by(idLoan=loan.id)
			shares = []
			for sha in sharesA:
				e = sha.toJson()
				shares.append(e)
			from mailing import mail
			msg = Message("Tunke - Prestamo exitoso", sender="tunkestaff@gmail.com", recipients=[prospectiveClient.email1])
			msg.body = 'Hola'
			fullName = person.firstName + ' ' + person.fatherLastname
			accNumber = str(account.accountNumber)
			curName = str(currency.currencyName)
			amount = str(d['amount'])
			currencySymbol = str(currency.currencySymbol)
			msg.html = render_template('loans.html', name=fullName, accountNumber=accNumber, currency=curName, amount=amount)
			logging.debug('Rendered')
			rendered = render_template('calendar.html', shares=shares, currencySymbol=currencySymbol,totalAmortization=str(round(totalAmortization, 2)),totalInterest=str(round(totalInterest,2)),totalComission=str(round(totalComission,2)),totalShare=str(round(totalShare,2)))
			logging.debug('Pdfkit')
			pdf = pdfkit.from_string(rendered , False)
			logging.debug('PDF')
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
			logging.debug(str(e))
			return response, status.HTTP_400_BAD_REQUEST