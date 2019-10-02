import datetime
from models.person import Person
from models.prospectiveclient import ProspectiveClient
from models.client import Client
from models.blacklist import Blacklist
from models.account import Account
from resources.admin.security import AuthRequiredResource
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource
from flask import request
import status

class ProspectiveClientListResource(Resource):
    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        
        id_person = request_dict['id_person']
        email1 = request_dict['email1']
        email2 = request_dict['email2']
        cellphone1 = request_dict['cellphone1']
        cellphone2 = request_dict['cellphone2']
        last_enter_date = datetime.datetime.now()
        
        try:
            prospectiveclient = ProspectiveClient.query.filter_by(id_person=id_person).first()
            if not prospectiveclient:
                prospectiveclient = ProspectiveClient(id_person=id_person, email1=email1, email2=email2,
                                                  cellphone1=cellphone1, cellphone2=cellphone2,
                                                  last_enter_date=last_enter_date)
                prospectiveclient.enter_count = 1
                prospectiveclient.add(prospectiveclient)
                query = ProspectiveClient.query.get(prospectiveclient.id)
                result = query.get_json()
                return result, status.HTTP_201_CREATED
            else:
                prospectiveclient.email1 = email1
                prospectiveclient.email2 = email2
                prospectiveclient.cellphone1 = cellphone1
                prospectiveclient.cellphone2 = cellphone2
                prospectiveclient.last_enter_date = last_enter_date
                prospectiveclient.enter_count += 1
                prospectiveclient.update()
                
                query = ProspectiveClient.query.get(prospectiveclient.id)
                result = query.get_json()
                return result, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST
            