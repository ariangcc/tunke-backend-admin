from app import db
from models.utils import AddUpdateDelete

class SalesRecord(db.Model, AddUpdateDelete):
    __tablename__ = 'salesRecord'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100))
    requestDate = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    idRecordStatus = db.Column('idRecordStatus', db.ForeignKey('recordStatus.id'))
    idClient = db.Column('idClient', db.ForeignKey('client.id'))
    idProduct = db.Column('idProduct', db.ForeignKey('product.id'))