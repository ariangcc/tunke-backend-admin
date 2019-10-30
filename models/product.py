from app import db
from models.utils import AddUpdateDelete
from models.account import Account
from models.salesRecord import SalesRecord
class Product(db.Model, AddUpdateDelete):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(100))
	active = db.Column(db.Boolean)
	accounts = db.relationship(Account)
	salesRecords = db.relationship(SalesRecord)

	def toJson(self):
		d = {}
		d['idProduct'] = self.id
		d['name'] = self.name
		d['description'] = self.description
		d['active'] = self.active
		return d