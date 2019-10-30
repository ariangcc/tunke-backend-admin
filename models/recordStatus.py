from app import db
from models.utils import AddUpdateDelete

class RecordStatus(db.Model, AddUpdateDelete):
	__tablename__ = 'recordStatus'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	salesRecords = db.relationship("SalesRecord")

	def toJson(self):
		d = {}
		d['idRecordStatus'] = self.id
		d['name'] = self.name
		return d