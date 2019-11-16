from app import db
from models.utils import AddUpdateDelete

class Transaction(db.Model, AddUpdateDelete):
	__tablename__ = 'transaction'
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime)
	amount = db.Column(db.Float)
	idAccount = db.Column(db.Integer, db.ForeignKey('account.id'))
	idBankAccount = db.Column(db.Integer, db.ForeignKey('bankAccount.id'))
	active = db.Column(db.Integer)

	def toJson(self):
		d = {}
		d['idTransaction'] = self.id
		d['datetime'] = self.datetime.strftime('%Y-%m-%d')
		d['amount'] = self.amount
		d['idAccount'] = self.idAccount
		d['idBankAccount'] = self.idBankAccount
		d['active'] = self.active
		return d