from app import db
from models.utils import AddUpdateDelete

class AccountType(db.Model, AddUpdateDelete):
    __tablename__ ='accountType'
    id = db.Column(db.Integer, primary_key=True)
    typeName = db.Column(db.String(100))
    accounts = db.relationship("Account")

    def toJson(self):
        d = {}
        d['idAccountType'] = self.id
        d['typeName'] = self.typeName
        return d