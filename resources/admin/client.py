from app import db
from models.client import Client
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
import status

class ClientResource(AuthRequiredResource):
    def get(self, id):
        try:
            client = Client.query.get_or_404(id)
            prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
            person = Person.query.get_or_404(prospectiveClient.idPerson)
            d = {}
            d.update(client.toJson())
            d.update(prospectiveClient.toJson())
            d.update(person.toJson())
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class ClientListResource(AuthRequiredResource):
    def get(self):
        try:
            clients = Client.query.all()
            d = {}
            d['clients'] = []
            for client in clients:
                prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
                person = Person.query.get_or_404(prospectiveClient.idPerson)
                e = {}
                e.update(client.toJson())
                e.update(prospectiveClient.toJson())
                e.update(person.toJson())
                d['clients'].append(e)
            
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST