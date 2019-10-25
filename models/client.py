from app import db
from models.utils import AddUpdateDelete

class Client(db.Model, AddUpdateDelete):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    registerDate = db.Column(db.DateTime)
    totalAccounts = db.Column(db.Integer)
    activeLoans = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    idProspectiveClient = db.Column('idProspectiveClient', db.ForeignKey('prospectiveClient.id'))
    salesRecords = db.relationship('SalesRecord')
    accounts = db.relationship('Account')

    def toJson(self):
        d = {}
        d['idClient'] = self.id
        d['registerDate'] = self.registerDate.strftime('%d-%m-%Y')
        d['totalAccount'] = self.totalAccounts
        d['activeLoans'] = self.activeLoans
        d['active'] = self.active
        d['idProspectiveClient'] = self.idProspectiveClient
        return d