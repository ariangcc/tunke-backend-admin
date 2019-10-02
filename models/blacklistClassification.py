from app import db
from models.utils import AddUpdateDelete

class BlacklistClassification(db.Model, AddUpdateDelete):
    __tablename__ = 'blacklistClassification'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    blacklists = db.relationship("Blacklist")