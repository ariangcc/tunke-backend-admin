from marshmallow import Schema, fields, pre_load
from marshmallow import Schema, fields
from models.product import Product
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from app import db

ma = Marshmallow()
locales = ['es_ES', 'es']

class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()
    
    def update(self):
        return db.session.commit()
    
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Account(db.Model, AddUpdateDelete):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True)
    balance = db.Column(db.Float)
    opening_date = db.Column(db.DateTime)
    closing_date = db.Column(db.DateTime)
    card_number = db.Column(db.String(16))
    id_account_type = db.Column(db.Integer, db.ForeignKey('accounttype.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('product.id'))
    id_currency = db.Column('id_currency', db.ForeignKey('currency.id'))
    transactions = db.relationship("Transaction")