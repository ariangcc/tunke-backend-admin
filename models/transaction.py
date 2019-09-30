from marshmallow import Schema, fields, pre_load
from marshmallow import Schema, fields
from models.account import Account
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

class Transaction(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'))