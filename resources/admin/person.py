from app import db
from models.person import Person
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
import status

class PersonResource(AuthRequiredResource):
    def get(self, id):
        try:
            person = Person.query.get_or_404(id)
            d = person.toJson()
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class PersonListResource(AuthRequiredResource):
    def get(self):
        try:
            persons = Person.query.all()
            d = []
            for person in persons:
                e = person.toJson()
                d.append(e)
            
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST