from app import db
from models.blacklist import Blacklist
from models.person import Person
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
import status

class BlackListListResource(AuthRequiredResource):
    def get(self):
        try:
            listBlackList = Blacklist.query.all()
            d = []
            for bl in listBlackList:
                bl = bl.toJson()
                person = Person.query.filter_by(documentNumber=bl['documentNumber']).first()
                d.append(person.toJson())
            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST