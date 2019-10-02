from models.account import Account
from models.accounttype import AccountType
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
import status


class AccountResource(AuthRequiredResource):
    def get(self, id):
        try:
            account = Account.get_or_404(id)
            d = {}
            #getjson for account
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class AccountListResource(AuthRequiredResource):
    def get(self):
        try:
            accounts = Accounts.query.all()
            l = []
            for account in accounts:
                d = {}
                #getjson for account
                l.append(d)
            
            return l, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST