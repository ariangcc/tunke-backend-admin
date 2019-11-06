from app import db
from models.utils import AddUpdateDelete

class Loan(db.Model, AddUpdateDelete):
    __tablename__ = 'loan'
    id = db.Column(db.Integer, primary_key=True)
    totalShares = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    interestRate = db.Column(db.Integer)
    idCampaign = db.Column('idCampaign', db.ForeignKey('campaign.id'))
    idClient = db.Column('idClient', db.ForeignKey('client.id'))
    idSalesRecord = db.Column('idSalesRecord', db.ForeignKey('salesRecord.id'))
    idShareType = db.Column('idShareType', db.ForeignKey('shareType.id'))
    active = db.Column(db.Integer)

    def toJson(self):
        d = {}
        d['idLoan'] = self.id
        d['totalShares'] = self.totalShares
        d['amount'] = self.amount
        d['interestRate'] = self.interestRate
        d['idCampaign'] = self.idCampaign
        d['idClient'] = self.idClient
        d['idSalesRecord'] = self.idSalesRecord
        d['idShareType'] = self.idShareType
        d['active'] = self.active
        return d

        