from app import db
from models.utils import AddUpdateDelete

class Transaction(db.Model, AddUpdateDelete):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    idAccount = db.Column(db.Integer, db.ForeignKey('account.id'))