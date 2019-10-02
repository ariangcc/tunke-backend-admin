from app import db
from models.utils import AddUpdateDelete

class Profile(db.Model, AddUpdateDelete):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    charge = db.Column(db.String(100), unique=True)
    users = db.relationship("User")