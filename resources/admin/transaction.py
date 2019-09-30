from models.transaction import Transaction
from models.account import Account
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
import status

class TransactionResource(AuthRequiredResource):
    def get(self, id):
        try:
            transaction = Transaction.get_or_404(id)
            d = {}
            d['id'] = transaction.id
            d['datetime'] = transaction.datetime
            d['amount'] = transaction.amount
            d['account_number'] = Account.get_or_404(transaction.id_account).account_number
            return d, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class TransactionListResource(AuthRequiredResource):
    def get(self):
        try:
            transactions = Transaction.query.all()
            l = []
            for transaction in transcations:
                d = {}
                d['id'] = transaction.id
                d['datetime'] = transaction.datetime
                d['amount'] = transaction.amount
                d['account_number'] = Account.get_or_404(transaction.id_account).account_number
                l.append(d)
            return l, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST