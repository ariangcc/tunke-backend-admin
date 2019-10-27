from app import db
from datetime import datetime
from models.account import Account
from models.accountType import AccountType
from models.client import Client
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from models.currency import Currency
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
import status


class AccountResource(AuthRequiredResource):
    def get(self, id):
        try:
            account = Account.query.get_or_404(id)
            client = Client.query.get_or_404(account.idClient)
            prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
            person = Person.query.get_or_404(prospectiveClient.idPerson)
            currency = Currency.query.get_or_404(account.idCurrency)
            accountType = AccountType.query.get_or_404(account.idAccountType)
            d = {}
            d['firstName'] = person.firstName
            d['middleName'] = person.middleName
            d['fatherLastname'] = person.fatherLastname
            d['motherLastname'] = person.motherLastname
            d['active'] = account.active and client.active
            d.update(account.toJson())
            d.update(currency.toJson())
            d.update(accountType.toJson())
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST
    
    def delete(self, id):
        try:
            account = Account.query.get_or_404(id)
            account.active = 0
            account.closingDate = datetime.now()
            account.update()
            db.session.commit()
            resp = {'ok': 'Cuenta borrada satisfactoriamente.'}
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class AccountListResource(AuthRequiredResource):
    def get(self):
        try:
            accounts = Account.query.all()
            d = {}
            d['accounts'] = []
            for account in accounts:
                client = Client.query.get_or_404(account.idClient)
                prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
                person = Person.query.get_or_404(prospectiveClient.idPerson)
                currency = Currency.query.get_or_404(account.idCurrency)
                accountType = AccountType.query.get_or_404(account.idAccountType)
                e = {}
                e['firstName'] = person.firstName
                e['middleName'] = person.middleName
                e['fatherLastname'] = person.fatherLastname
                e['motherLastname'] = person.motherLastname
                e['active'] = account.active and client.active
                e.update(account.toJson())
                e.update(currency.toJson())
                e.update(accountType.toJson())
                d['accounts'].append(e)
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST