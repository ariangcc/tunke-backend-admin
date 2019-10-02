from marshmallow import Schema, fields, pre_load
from marshmallow import Schema, fields
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

class Blacklist_clasification(db.Model, AddUpdateDelete):
    __tablename__ = 'blacklist_clasification'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    blacklists = db.relationship("Blacklist")