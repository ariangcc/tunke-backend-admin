from datetime import datetime
from models.prospectiveclient import ProspectiveClient
from models.account import Account 
from models.accounttype import AccountType
from models.person import Person 
from models.client import Client
from resources.utils import GenerateAccount
from models.salesrecord import SalesRecord
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
import status
from flask import request
from app import db

class OpenAccountResource(Resource):
    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        curdatetime = datetime.now()
        try:
            id_person = request_dict['id_person']
            prospectiveclient = ProspectiveClient.query.filter_by(id_person=id_person).first()
            client = Client(register_date=curdatetime, total_accounts=1, active_loans=0, active=1, id_prospectiveclient=prospectiveclient.id)
            client.add(client)
            
            salesrecord = SalesRecord(origin="Origen default", active=1,request_date=curdatetime,id_client=client.id)
            salesrecord.add(salesrecord)

            currency = request_dict['currency']
            account = Account(account_number=GenerateAccount(), balance=0.0, opening_date=curdatetime, 
                              closing_date=None, card_number="1234-5678-1234-5678", id_account_type=1,
                              id_product=1, id_currency=currency)
            account.add(account)

            reg_client = Client.query.get(client.id)
            reg_account = Account.query.get(account.id)
            person = Person.query.get(prospectiveclient.id_person)
            d = {}
            d['name'] = " ".join([person.first_name, person.middle_name, person.father_lastname, person.mother_lastname])
            d['account_number'] = reg_account.account_number
            d['cci'] = "0011-" + reg_account.account_number
            d['account_detail'] = 'Cuenta Simple'
            d['opening_date'] = reg_account.opening_date.strftime('%d-%m-%Y')
            d['currency'] = ('Soles' if reg_account.id_currency == 1 else 'Dolares')
            d['email'] = prospectiveclient.email1
            db.session.commit()
            return d, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST