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

class OpenAccountResource(Resource):
    def post(self):
        requestDict = request.get_json()
        if not requestDict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        curdatetime = datetime.now()
        try:
            idPerson = requestDict['idPerson']
            prospectiveClient = ProspectiveClient.query.filter_by(idPerson=idPerson).first()
            client = Client(registerDate=curdatetime, totalAccounts=1, activeLoans=0, active=1, idProspectiveClient=prospectiveClient.id)
            client.add(client)
            
            salesRecord = SalesRecord(origin="Origen default", active=1,requestDate=curdatetime,idClient=client.id)
            salesRecord.add(salesRecord)
            currency = requestDict['currency']
            account = Account(accountNumber=GenerateAccount(), balance=0.0, openingDate=curdatetime, 
                              closingDate=None, cardNumber="1234-5678-1234-5678", idAccountType=1,
                              idProduct=1, idCurrency=currency)
            account.add(account)

            #Commit changes
            db.session.commit()

            regClient = Client.query.get(client.id)
            regAccount = Account.query.get(account.id)
            person = Person.query.get(prospectiveClient.idPerson)
            d = {}
            d['name'] = " ".join([person.firstName, person.middleName, person.fatherLastname, person.motherLastname])
            d['accountNumber'] = regAccount.accountNumber
            d['cci'] = "0011-" + regAccount.accountNumber
            d['accountDetail'] = 'Cuenta Simple'
            d['openingDate'] = regAccount.openingDate.strftime('%d-%m-%Y')
            d['currency'] = ('Soles' if regAccount.idCurrency == 1 else 'Dolares')
            d['email'] = prospectiveClient.email1

            from mailing import mail
            msg = Message("Tunke - Apertura de cuenta exitosa", sender="tunkestaff@gmail.com", recipients=[d['email']])
            msg.body = 'Hola'
            msg.html = render_template('ejemplo.html', name=d['name'], accountNumber=d['accountNumber'], cci=d['cci'], accountDetail=d['accountDetail'],
                                        openingDate=d['openingDate'], currency=d['currency'])
            mail.send(msg)
            return d, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST