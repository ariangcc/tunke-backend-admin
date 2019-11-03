from app import db
from resources.admin.security import AuthRequiredResource
from models.salesRecord import SalesRecord
from models.recordStatus import RecordStatus
from models.client import Client
from models.product import Product
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from models.account import Account
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
import status
from datetime import datetime
import requests, json

class SalesRecordListResource(AuthRequiredResource):
    def get(self):
        try:
            salesRecords = SalesRecord.query.all()
            d = {}
            d['salesRecords'] = []
            for salesRecord in salesRecords:
                salesRecord = salesRecord.toJson()
                recordStatus = RecordStatus.query.get_or_404(salesRecord['idRecordStatus'])
                client = Client.query.get_or_404(salesRecord['idClient'])
                product = Product.query.get_or_404(salesRecord['idProduct'])
                client = client.toJson()
                prospectiveClient = ProspectiveClient.query.get_or_404(client['idProspectiveClient'])
                prospectiveClient = prospectiveClient.toJson()
                person = Person.query.get_or_404(prospectiveClient['idPerson'])
                account = Account.query.filter_by(idSalesRecord=salesRecord['idSalesRecord']).first()
                person = person.toJson()
                product = product.toJson()
                account = account.toJson()
                recordStatus = recordStatus.toJson()
                e = {}
                e['activeAccount'] = account['active']
                e['activeClient'] = client['active']
                e['nameRecordStatus'] = recordStatus['name']
                e['fullName'] = person['firstName'] + ' '+ person['fatherLastname']
                e['documentNumber'] = person['documentNumber']
                e['idSalesRecord'] = salesRecord['idSalesRecord']
                e['origin'] = salesRecord['origin']
                e['requestDate'] = salesRecord['requestDate']
                e['activeSalesRecord'] = salesRecord['active']
                e['productName'] = product['name']
                d['salesRecords'].append(e)
            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error',str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error',str(e)}
            return response, status.HTTP_400_BAD_REQUEST


