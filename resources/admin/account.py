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
            d['id'] = account.id
            d['account_number'] = account.account_number
            d['balance'] = account.balance
            d['opening_date'] = account.opening_date
            d['closing_date'] = account.closing_date
            d['card_number'] = account.card_number
            d['account_type'] =  AccountType.get_or_404(account.id_account_type).type_name
            #d['product_name'] = account.name
            #d['product_description'] = account.description 
            #d['active'] = account.active
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
                d['id'] = account.id
                d['account_number'] = account.account_number
                d['balance'] = account.balance
                d['opening_date'] = account.opening_date
                d['closing_date'] = account.closing_date
                d['card_number'] = account.card_number
                d['account_type'] =  AccountType.get_or_404(account.id_account_type).type_name
                #d['product_name'] = account.name
                #d['product_description'] = account.description 
                #d['active'] = account.active
                l.append(d)
            
            return l, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST