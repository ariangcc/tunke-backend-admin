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

class AccountType(db.Model, AddUpdateDelete):
    __tablename__ ='accounttype'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100))
    accounts = db.relationship("Account")

class AccountTypeSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    type_name = fields.String(required=True)