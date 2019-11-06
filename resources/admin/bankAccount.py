from app import db
from models.bankAccount import BankAccount
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
import status

class BankAccountResource(AuthRequiredResource):
    def get(self):
        try:
            bankAccount = BankAccount.query.filter_by(id=1).first()
            d = bankAccount.toJson()
            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST