from models.user import User, UserSchema
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
import status

user_schema = UserSchema()

class UserResource(AuthRequiredResource):
    def get(self, id):
        try:
            user = User.get_or_404(id)
            d = {}
            d['id'] = user.id
            d['email'] = user.email
            
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class UserListResource(AuthRequiredResource):
    def get(self):
        try:
            users = User.query.all()
            d = []
            for user in users:
                e = {}
                e['id'] = user.id
                e['email'] = user.email
                d.append(e)
            
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST