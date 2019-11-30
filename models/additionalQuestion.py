from app import db
from models.utils import AddUpdateDelete

class AdditionalQuestion(db.Model, AddUpdateDelete):
    __tablename__ = 'additionalQuestion'
    id = db.Column(db.Integer, primary_key=True)
    response1 = db.Column(db.String(500))
    response2 = db.Column(db.String(500))
    response3 = db.Column(db.String(500))
    response4 = db.Column(db.String(500))
    idAccount = db.Column(db.Integer, db.ForeignKey('account.id'))

    def toJson(self):
        d = {}
        d['idAdditionalQuestion'] = self.id
        d['response1'] = self.response1
        d['response2'] = self.response2
        d['response3'] = self.response3
        d['response4'] = self.response4
        d['idAccount'] = self.idAccount
        return d