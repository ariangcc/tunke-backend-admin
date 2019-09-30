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

class ProspectiveClient(db.Model, AddUpdateDelete):
    __tablename__ = 'prospectiveclient'
    id = db.Column(db.Integer, primary_key=True)
    last_enter_date = db.Column(db.DateTime)
    enter_count = db.Column(db.Integer)
    email1 = db.Column(db.String(100))
    email2 = db.Column(db.String(100))
    cellphone1 = db.Column(db.String(20))
    cellphone2 = db.Column(db.String(20))
    id_person = db.Column('id_person', db.ForeignKey('person.id'))