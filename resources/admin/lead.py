from app import db
from models.lead import Lead
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
import status

class LeadResource(AuthRequiredResource):
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