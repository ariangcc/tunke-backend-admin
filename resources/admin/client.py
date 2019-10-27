from app import db
from models.client import Client
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
import status
from datetime import datetime

class ClientResource(AuthRequiredResource):
    def get(self, id):
        try:
            client = Client.query.get_or_404(id)
            prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
            person = Person.query.get_or_404(prospectiveClient.idPerson)
            d = {}
            nationality = requests.get('https://restcountries.eu/rest/v2/alpha/col')
            d.update(client.toJson())
            d.update(prospectiveClient.toJson())
            d.update(person.toJson())
            d['nationality'] = nationality['name']
            d['flag'] = nationality['flag']
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

    def put(self, id): 
        try:
            requestDict = request.get_json()
            if not requestDict:
                response = {'error': 'No input data provided'}
                return response, status.HTTP_400_BAD_REQUEST
            
            client = Client.query.get_or_404(id)

            #Datos para el prospecto
            email1 = requestDict['email1']
            email2 = requestDict['email2']
            cellphone1 = requestDict['cellphone1']
            cellphone2 = requestDict['cellphone2']
            lastEnterDate = datetime.now()
            
            prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)

            if not prospectiveClient:
                resp = {'error': 'No existe el cliente a actualizar. Revise el flujo.'}
                return resp, status.HTTP_400_BAD_REQUEST
        
            prospectiveClient.email1 = email1
            prospectiveClient.email2 = email2
            prospectiveClient.cellphone1 = cellphone1
            prospectiveClient.cellphone2 = cellphone2
            prospectiveClient.lastEnterDate = lastEnterDate
            prospectiveClient.enterCount += 1
            prospectiveClient.update()
            
            #Commit registro de prospecto
            db.session.commit()

            resp = {'ok': 'Cliente actualizado con exito.'}

            return resp, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        try:
            client = Client.query.get_or_404(id)
            client.active = 0
            client.update()
            db.session.commit()
            resp = {'ok': 'Cliente borrado satisfactoriamente.'}
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
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
    
    def post(self):
        try:
            requestDict = request.get_json()
            if not requestDict:
                response = {'error': 'No input data provided'}
                return response, status.HTTP_400_BAD_REQUEST
            
            # Datos para la cuenta
            idPerson = requestDict['idPerson']

            #Datos para el prospecto
            email1 = requestDict['email1']
            email2 = requestDict['email2']
            cellphone1 = requestDict['cellphone1']
            cellphone2 = requestDict['cellphone2']
            lastEnterDate = datetime.now()

            prospectiveClient = ProspectiveClient.query.filter_by(idPerson=idPerson).first()
            if not prospectiveClient:
                prospectiveClient = ProspectiveClient(idPerson=idPerson, email1=email1, email2=email2,
                                                  cellphone1=cellphone1, cellphone2=cellphone2,
                                                  lastEnterDate=lastEnterDate)
                prospectiveClient.enterCount = 1
                prospectiveClient.add(prospectiveClient)
            else:
                prospectiveClient.email1 = email1
                prospectiveClient.email2 = email2
                prospectiveClient.cellphone1 = cellphone1
                prospectiveClient.cellphone2 = cellphone2
                prospectiveClient.lastEnterDate = lastEnterDate
                prospectiveClient.enterCount += 1
                prospectiveClient.update()
            
            #Commit registro de prospecto
            db.session.commit()

            client = Client(registerDate=lastEnterDate, totalAccounts=0, activeLoans=0, active=1, idProspectiveClient=prospectiveClient.id)
            client.add(client)
            
            #Commit registro de cliente 
            db.session.commit()

            resp = {'ok': 'Cliente registrado con exito.'}

            return resp, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST
    