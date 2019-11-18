from app import db
from models.lead import Lead
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
import status

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

            lead = Lead(idClient=idClient,idCampaign=idCampaign,minimumLoan=minimumLoan,maximumLoan=maximumLoan,active=1)
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