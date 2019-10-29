import random
from datetime import datetime
from models.prospectiveClient import ProspectiveClient
from models.account import Account 
from models.accountType import AccountType
from models.person import Person 
from models.client import Client
from resources.utils import GenerateAccount
from models.salesRecord import SalesRecord
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
import status
from flask import request, render_template
from flask_mail import Message
from app import db

class SendTokenResource(Resource):
    def post(self):
        try:
            requestDict = request.get_json()
            if not requestDict:
                response = {'error': 'No input data provided'}
                return response, status.HTTP_400_BAD_REQUEST

            email = requestDict['email']

            randomToken = "".join(chr(x) for x in [random.randint(ord('A'), ord('Z')) for _ in range(6)])

            from mailing import mail
            msg = Message("Tunke - Token Apertura de Cuenta", sender="tunkestaff@gmail.com", recipients=[email])
            msg.body = "Su token es " + randomToken
            mail.send(msg)
            d = {"token": randomToken}
            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST