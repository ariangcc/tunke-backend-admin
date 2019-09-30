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

class Currency(db.Model, AddUpdateDelete):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String(100), unique=True)
    currency_symbol = db.Column(db.String(5), unique=True)
    currency_code = db.Column(db.String(3), unique=True)
    accounts = db.relationship("Account")