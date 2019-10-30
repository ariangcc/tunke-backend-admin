from app import db
from models.utils import AddUpdateDelete

class Person(db.Model, AddUpdateDelete):
	__tablename__ = 'person'
	id = db.Column(db.Integer, primary_key=True)
	documentType = db.Column(db.String(100))
	documentNumber = db.Column(db.String(20), unique=True)
	firstName = db.Column(db.String(100))
	middleName = db.Column(db.String(100))
	fatherLastname = db.Column(db.String(100))
	motherLastname = db.Column(db.String(100))
	birthdate = db.Column(db.DateTime)
	address = db.Column(db.String(100))
	nationality = db.Column(db.String(100))
	vehicle1Plate = db.Column(db.String(100))
	vehicle2Plate = db.Column(db.String(100))
	prospectiveClients = db.relationship("ProspectiveClient")

	def toJson(self):
		d = {}
		d['idPerson'] = self.id
		d['documentType'] = self.documentType
		d['documentNumber'] = self.documentNumber
		d['firstName'] = self.firstName
		d['middleName'] = self.middleName
		d['fatherLastname'] = self.fatherLastname
		d['motherLastname'] = self.motherLastname
		d['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
		d['address'] = self.address
		d['nationality'] = self.nationality
		d['vehicle1Plate'] = self.vehicle1Plate
		d['vehicle2Plate'] = self.vehicle2Plate
		
		return d