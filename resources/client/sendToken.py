import random
from datetime import datetime
from models.prospectiveClient import ProspectiveClient
from models.account import Account 
from models.accountType import AccountType
from models.person import Person 
from models.client import Client
from resources.utils import GenerateAccount, SendMail, SendSMS
from models.salesRecord import SalesRecord
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
import status
from flask import request, render_template
from app import db

class SendTokenResource(Resource):
	def post(self):
		try:
			requestDict = request.get_json()
			if not requestDict:
				response = {'error': 'No input data provided'}
				return response, status.HTTP_400_BAD_REQUEST

			msgType = int(requestDict['msgType'])
			randomCharacters = [chr(random.randint(ord('A'), ord('Z'))) for _ in range(3)]
			randomCharacters.extend(chr(random.randint(0, 9) + ord('0')) for _ in range(3))
			random.shuffle(randomCharacters)
			randomToken = "".join(x for x in randomCharacters)
			 
			if msgType == 1: #Envio por email
				email = requestDict['email']
				SendMail("Tunke - Token", "tunkestaff@gmail.com", email, "Su token es " + randomToken)
			else:
				cellphone = requestDict['cellphone']
				SendSMS(cellphone, "Su token es " + randomToken)

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
