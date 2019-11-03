from app import db
from models.utils import AddUpdateDelete

class ParameterSettings(db.Model, AddUpdateDelete):
	__tablename__ = 'parameterSettings'
	id = db.Column(db.Integer, primary_key=True)
	maxTokenSends = db.Column(db.Integer)
	maxDiaryMovements = db.Column(db.Integer)
	legalAge = db.Column(db.Integer)
	maxAccountsNumber = db.Column(db.Integer)

	def toJson(self):
		d = {}
		d['idParameterSettings'] = self.id
		d['maxTokenSends'] = self.maxTokenSends
		d['maxDiaryMovements'] = self.maxDiaryMovements
		d['legalAge'] = self.legalAge
		d['maxAccountsNumber'] = self.maxAccountsNumber
		
		return d