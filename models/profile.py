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

class Profile(db.Model, AddUpdateDelete):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    charge = db.Column(db.String(100), unique=True)