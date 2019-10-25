from models.person import Person
from models.prospectiveClient import ProspectiveClient
from models.client import Client
from models.blacklist import Blacklist
from models.account import Account
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request, jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError
from flask_mail import Message
import status
from app import db

class DniValidationResource(Resource):
    def post(self):
        requestDict = request.get_json()
        if not requestDict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        documentNumber = requestDict['documentNumber']
        try:
            blacklisted = (Blacklist.query.filter_by(documentNumber=documentNumber).first())
            d = {}
            if(blacklisted):
                d['type'] = 3
                return d, status.HTTP_200_OK
            else:
                person = (Person.query.filter_by(documentNumber=documentNumber).first())
                if not person:
                    d['error'] = "La persona ingresada no existe en los registros"
                    return d, status.HTTP_400_BAD_REQUEST

                prospectiveClient = (ProspectiveClient.query.filter_by(idPerson=person.id).first())

                if not prospectiveClient:
                    d['type'] = 2 #Es no cliente, aun no es prospecto
                    d.update(person.toJson())
                    return d, status.HTTP_200_OK
                
                client = (Client.query.filter_by(idProspectiveClient=prospectiveClient.id).first())

                if not client:
                    d['type'] = 2 #Es no cliente, ya es prospecto
                    d.update(person.toJson())
                    return d, status.HTTP_200_OK
                
                d['type'] = 1
                d.update(person.toJson())
                d.update(prospectiveClient.toJson())
                return d, status.HTTP_200_OK
            
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST
