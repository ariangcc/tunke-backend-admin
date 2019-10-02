from marshmallow import Schema, fields, pre_load
from marshmallow import Schema, fields
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

class Client(db.Model, AddUpdateDelete):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.DateTime)
    total_accounts = db.Column(db.Integer)
    active_loans = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    id_prospectiveclient = db.Column('id_prospectiveclient', db.ForeignKey('prospectiveclient.id'))
    salesrecords = db.relationship('SalesRecord')