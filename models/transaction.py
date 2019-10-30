from app import db
from models.utils import AddUpdateDelete

class Transaction(db.Model, AddUpdateDelete):
	__tablename__ = 'transaction'
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime)
	amount = db.Column(db.Float)
	idAccount = db.Column(db.Integer, db.ForeignKey('account.id'))

	def toJson(self):
		d = {}
		d['idTransaction'] = self.id
		d['datetime'] = self.datetime.strftime('%d-%m-%Y')
		d['amount'] = self.amount
		d['idAccount'] = self.idAccount
		return d