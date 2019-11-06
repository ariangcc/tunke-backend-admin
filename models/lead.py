from app import db
from models.utils import AddUpdateDelete

class Lead(db.Model, AddUpdateDelete):
    __tablename__ = 'lead'
    id = db.Column(db.Integer, primary_key=True)
    minimumLoan = db.Column(db.Integer)
    maximumLoan = db.Column(db.Integer)
    active = db.Column(db.Integer)
    idCampaign = db.Column('idCampaign', db.ForeignKey('campaign.id'))
    idClient = db.Column('idClient', db.ForeignKey('client.id'))

    def toJson(self):
        d = {}
        d['idLead'] = self.id
        d['minimumLoan'] = self.minimumLoan
        d['maximumLoan'] = self.maximumLoan
        d['active'] = self.active
        d['idCampaign'] = self.idCampaign
        d['idClient'] = self.idClient
        return d
        