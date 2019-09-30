from models.account import Account
from models.accounttype import AccountType
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
import status
from flask import request

class OpenAccountResource(AuthRequiredResource):
    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        try:
            result = {"ok": "tudo bem"}
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST