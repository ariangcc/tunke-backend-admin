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
    prospectiveclients = db.relationship("ProspectiveClient")

    def get_json(self):
        d = {}
        d['id_person'] = self.id
        d['document_type'] = self.document_type
        d['document_number'] = self.document_number
        d['first_name'] = self.first_name
        d['middle_name'] = self.middle_name
        d['father_lastname'] = self.father_lastname
        d['mother_lastname'] = self.mother_lastname
        d['birthdate'] = self.birthdate.strftime('%d-%m-%Y')
        d['address'] = self.address
        d['nationality'] = self.nationality
        d['vehicle1_plate'] = self.vehicle1_plate
        d['vehicle2_plate'] = self.vehicle2_plate
        
        return d