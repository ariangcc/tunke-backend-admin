from models.person import Person
from models.prospectiveclient import ProspectiveClient
from models.client import Client
from models.blacklist import Blacklist
from models.account import Account
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import status

class DniValidationResource(Resource):
    def get(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        
        document_number = request_dict['document_number']
        try:
            blacklisted = (Blacklist.query.filter_by(document_number=document_number).first())
            d = {}
            if(blacklisted):
                d['tipo'] = 3
                return d, status.HTTP_200_OK
            else:
                person = (Person.query.filter_by(document_number=document_number).first())
                if not person:
                    d['error'] = "La persona ingresada no existe en los registros"
                    return d, status.HTTP_400_BAD_REQUEST

                prospectiveclient = (ProspectiveClient.query.filter_by(id_person=person.id).first())

                if not prospectiveclient:
                    d['tipo'] = 2 #Es no cliente, aun no es prospecto
                    d.update(person.get_json())
                    return d, status.HTTP_200_OK
                
                client = (Client.query.filter_by(id_prospectiveclient=prospectiveclient.id).first())

                if not client:
                    d['tipo'] = 2 #Es no cliente, ya es prospecto
                    d.update(person.get_json())
                    return d, status.HTTP_200_OK
                
                d['tipo'] = 1
                d.update(person.get_json())
                d.update(prospectiveclient.get_json())
                return d, status.HTTP_200_OK
            
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST