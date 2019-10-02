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
    clients = db.relationship("Client")

    def get_json(self):
        d = {}
        d['id_prospectiveclient'] = self.id
        d['last_enter_date'] = self.last_enter_date.strftime('%d-%m-%Y')
        d['enter_count'] = self.enter_count
        d['email1'] = self.email1
        d['email2'] = self.email2
        d['cellphone1'] = self.cellphone1
        d['cellphone2'] = self.cellphone2

        return d