from app import db
from models.utils import AddUpdateDelete

class Account(db.Model, AddUpdateDelete):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    accountNumber = db.Column(db.String(100), unique=True)
    balance = db.Column(db.Float)
    openingDate = db.Column(db.DateTime)
    closingDate = db.Column(db.DateTime)
    cardNumber = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    idAccountType = db.Column(db.Integer, db.ForeignKey('accountType.id'))
    idProduct = db.Column(db.Integer, db.ForeignKey('product.id'))
    idCurrency = db.Column('idCurrency', db.ForeignKey('currency.id'))
    idClient = db.Column('idClient', db.ForeignKey('client.id'))
    transactions = db.relationship("Transaction")

    def toJson(self):
        d = {}
        d['idAccount'] = self.id
        d['accountNumber'] = self.accountNumber
        d['balance'] = self.balance
        d['openingDate'] = self.openingDate.strftime('%d-%m-%Y')
        d['closingDate'] = (self.closingDate.strftime('%d-%m-%Y') if self.closingDate is not None else "UNDEFINED")
        d['cardNumber'] = self.cardNumber
        d['idAccountType'] = self.idAccountType
        d['idProduct'] = self.idProduct
        d['idCurrency'] = self.idCurrency
        d['idClient'] = self.idClient
        return d