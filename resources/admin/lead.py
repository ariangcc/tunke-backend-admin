from app import db
from models.lead import Lead
from models.client import Client
from models.prospectiveClient import ProspectiveClient
from models.person import Person
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
import status
import pandas as pd
import requests ,json

class LeadResource(Resource):
    def get(self,id):
        try:
            lead = Lead.query.get_or_404(id)
            return lead.toJson(), status.HTTP_200_OK
        
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class LeadListResource(AuthRequiredResource):
    def post(self):
        requestDict = request.get_json()
        try :
            if not requestDict:
                response = {'error': 'No input data provided'}
                return response, status.HTTP_400_BAD_REQUEST

            idClient = requestDict['idClient']
            idCampaign = requestDict['idCampaign']
            minimumLoan = requestDict['minimumLoan']
            maximumLoan = requestDict['maximumLoan']
            minimumPeriod = requestDict['minimumPeriod']
            maximumPeriod = requestDict['maximumPeriod']
            interestRate = requestDict['interestRate']

            lead = Lead(idClient=idClient,idCampaign=idCampaign,minimumLoan=minimumLoan,maximumLoan=maximumLoan,active=1,minimumPeriod=minimumPeriod,maximumPeriod=maximumPeriod,interestRate=interestRate)
            lead.add(lead)

            db.session.commit()
            response = {'ok' : 'Lead creado correctamente'}
            return response, status.HTTP_201_CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST

    def put(self):
        try:
            file = request.files['file']
            if file.filename == '':
                response = {'error' : 'No selected files'}
                return response, status.HTTP_400_BAD_REQUEST
            
            if not file or not allowed_file(file.filename):
                response = {'error': 'Corrupt file or bad file extension'}
                return response, status.HTTP_400_BAD_REQUEST
            
            # File correcta aqui
            try:
                df = pd.read_csv(file.data, header=0, skip_blank_lines=True, 
                        skipinitialspace=True, encoding='latin-1')
            except:
                df = pd.read_excel(file.data, header=None)
            
            n = df[0].size
            response = {}
            response['badIndexes'] = []
            response['badReasons'] = []
            
            for i in range(n):
                documentNumber = df[0][i]
                productType = df[1][i]
                currency = df[2][i]
                minimumAmount = df[3][i]
                maximumAmount = df[4][i]
                minimumTerm = df[5][i]
                maximumTerm = df[6][i]
                interestRate = df[7][i]
                if isinstance(documentNumber, float):
                    documentNumber = fixDocumentNumber(str(int(documentNumber)))

            response = {'ok': 'Datos agregados correctamente'}
            return response, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class GetByCampaignResource(AuthRequiredResource):
    def post(self):
        try:
            requestDict = request.get_json()
            if not requestDict:
                response = {'error': 'No input data provided'}
                return response, status.HTTP_400_BAD_REQUEST

            idCampaign = requestDict['idCampaign']

            leads = Lead.query.filter_by(idCampaign=idCampaign)
            d = {}
            d['leads'] = []
            for lead in leads:
                e = lead.toJson()
                client = Client.query.get_or_404(e['idClient'])
                prospectiveClient = ProspectiveClient.query.get_or_404(client.idProspectiveClient)
                person = Person.query.get_or_404(prospectiveClient.idPerson)
                person = person.toJson()
                nationality = json.loads(requests.get('https://restcountries.eu/rest/v2/alpha/' + person['nationality']).text)
                e['nationality'] = nationality['name']
                e['flag'] = nationality['flag']
                e['documentNumber'] = person['documentNumber']
                e['firstName'] = person['firstName']
                e['middleName'] = person['middleName']
                e['fatherLastname'] = person['fatherLastname']
                e['motherLastname'] = person['motherLastname']
                e['birthdate'] = person['birthdate']
                e['address'] = person['address']
                d['leads'].append(e)

            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST