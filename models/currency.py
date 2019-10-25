from app import db
from models.utils import AddUpdateDelete

class Currency(db.Model, AddUpdateDelete):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    currencyName = db.Column(db.String(100), unique=True)
    currencySymbol = db.Column(db.String(5), unique=True)
    currencyCode = db.Column(db.String(3), unique=True)
    accounts = db.relationship("Account")

    def toJson(self):
        d = {}
        d['idCurrency'] = self.id
        d['currencyName'] = self.currencyName
        d['currencySymbol'] = self.currencySymbol
        d['currencyCode'] = self.currencyCode
        return d