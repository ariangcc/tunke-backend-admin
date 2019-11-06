from app import db
from models.loan import Loan
from models.client import Client
from models.salesRecord import SalesRecord
from models.account import Account
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
				account.balance = account.balance + loan.amount
				client.activeLoans = 1
			elif state == 2:
				salesRecord.idRecordStatus = 2
				client.activeLoans = 0

			salesRecord.update()
			client.update()
			account.update()
			db.session.commit()
			response = {'ok': 'Prestamo actualizado satisfactoriamente.'}
			return response, status.HTTP_204_NO_CONTENT

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
				e = loan.toJson()
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

