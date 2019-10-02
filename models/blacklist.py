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

class Blacklist(db.Model, AddUpdateDelete):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(100))
    document_number = db.Column(db.String(20), unique=True)
    active = db.Column(db.Boolean)
    id_blacklist_clasification = db.Column('id_blacklist_clasification', db.ForeignKey('blacklist_clasification.id'))