from app import db
from models.client import Client
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
import status

class ClientResource(AuthRequiredResource):
    def get(self, id):
        try:
            client = Client.query.get_or_404(id)
            d = client.toJson()
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class ClientListResource(AuthRequiredResource):
    def get(self):
        try:
            clients = Client.query.all()
            d = []
            for client in clients:
                e = client.toJson()
                d.append(e)
            
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST