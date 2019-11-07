from app import db
from models.utils import AddUpdateDelete

class BankAccount(db.Model, AddUpdateDelete):
    __tablename__ = 'bankAccount'
    id = db.Column(db.Integer, primary_key=True)
    accountNumber = db.Column(db.String(100))
    balance = db.Column(db.Float)
    idCurrency = db.Column('idCurrency', db.ForeignKey('currency.id'))
    active = db.Column(db.Integer)

    def toJson(self):
        d = {}
        d['idBankAccount'] = self.id
        d['accountNumber'] = self.accountNumber
        d['balance'] = self.balance
        d['idCurrency'] = self.idCurrency
        d['active'] = self.active
        return d