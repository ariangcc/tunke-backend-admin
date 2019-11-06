from app import db
from models.loan import Loan
from models.client import Client
from models.salesRecord import SalesRecord
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import status

class LoanResource(AuthRequiredResource):
	def get(self, id):
		try:
			loan = Loan.query.get_or_404(id)
			d = loan.toJson()
			return d, status.HTTP_200_OK

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
			d = []
			for loan in loans:
				e = loan.toJson()
				d.append(e)

			return d, status.HTTP_200_OK

		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error', str(e)}
			return response, status.HTTP_400_BAD_REQUEST