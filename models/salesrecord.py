from marshmallow import Schema, fields, pre_load
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from models.recordstatus import RecordStatus
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

class SalesRecord(db.Model, AddUpdateDelete):
    __tablename__ = 'salesrecord'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100))
    request_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    id_recordstatus = db.Column('id_recordstatus', db.ForeignKey(RecordStatus.id))
    products = db.relationship("Product")