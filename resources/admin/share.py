from app import db
from models.share import Share
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
import status

class ShareListResource(AuthRequiredResource):
	def get(self):
		try:
			shares = Share.query.filter_by(idLoan=65)
			d = []
			for share in shares:
				e = share.toJson()
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