from app import db
from models.utils import AddUpdateDelete

class ProspectiveClient(db.Model, AddUpdateDelete):
	__tablename__ = 'prospectiveClient'
	id = db.Column(db.Integer, primary_key=True)
	lastEnterDate = db.Column(db.DateTime)
	enterCount = db.Column(db.Integer)
	email1 = db.Column(db.String(100))
	email2 = db.Column(db.String(100))
	cellphone1 = db.Column(db.String(20))
	cellphone2 = db.Column(db.String(20))
	idPerson = db.Column('idPerson', db.ForeignKey('person.id'))
	clients = db.relationship("Client")

	def toJson(self):
		d = {}
		d['idProspectiveClient'] = self.id
		d['lastEnterDate'] = self.lastEnterDate.strftime('%d-%m-%Y')
		d['enterCount'] = self.enterCount
		d['email1'] = self.email1
		d['email2'] = self.email2
		d['cellphone1'] = self.cellphone1
		d['cellphone2'] = self.cellphone2

		return d