from app import db
from models.lead import Lead
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
import status

class LeadResource(AuthRequiredResource):
    def post(self):
        requestDict = request.get_json()
        if not requestDict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        idClient = requestDict['idClient']
        idCampaign = requestDict['idCampaign']
        try:
            d = {}
            lead = Lead.query.filter_by(idClient=idClient,idCampaign=idCampaign).first()
            d['lead'] = lead.toJson()
            return d, status.HTTP_200_OK
        
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST