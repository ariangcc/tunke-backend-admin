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

class Person(db.Model, AddUpdateDelete):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(100))
    document_number = db.Column(db.String(20), unique=True)
    first_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    father_lastname = db.Column(db.String(100))
    mother_lastname = db.Column(db.String(100))
    birthdate = db.Column(db.DateTime)
    address = db.Column(db.String(100))
    nationality = db.Column(db.String(100))
    vehicle1_plate = db.Column(db.String(100))
    vehicle2_plate = db.Column(db.String(100))

