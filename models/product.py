from marshmallow import Schema, fields, pre_load
from marshmallow import Schema, fields
from models.salesrecord import SalesRecord
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from app import db

class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()
    
    def update(self):
        return db.session.commit()
    
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Product(db.Model, AddUpdateDelete):
    id_salesrecord = db.Column('id_salesrecord', db.ForeignKey(SalesRecord.id)) 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    accounts = db.relationship('Account', backref = 'account')