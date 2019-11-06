from app import db
from models.utils import AddUpdateDelete

class ShareType(db.Model, AddUpdateDelete):
	__tablename__ = 'shareType'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	description = db.Column(db.String(255))
	active = db.Column(db.Integer)
	loans = db.relationship("Loan")

	def toJson(self):
		d = {}
		d['idShareType'] = self.id
		d['name'] = self.name
		d['description'] = self.description
		d['active'] = self.active
		return d

		