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
    idAccountType = db.Column(db.Integer, db.ForeignKey('accountType.id'))
    idProduct = db.Column(db.Integer, db.ForeignKey('product.id'))
    idCurrency = db.Column('idCurrency', db.ForeignKey('currency.id'))
    transactions = db.relationship("Transaction")