from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from marshmallow import Schema, fields
from marshmallow_validators.wtforms import from_wtforms
from wtforms.validators import Email, Length
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from app import db
from passlib.apps import custom_app_context as password_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from models.utils import AddUpdateDelete

class User(UserMixin, AddUpdateDelete, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	name = db.Column(db.String(100))
	password = db.Column(db.String(100))
	idProfile = db.Column('idProfile', db.ForeignKey('profile.id'))

	def GenerateAuthToken(self, expiration = 600):
		s = Serializer('hola', expires_in = expiration)
		return s.dumps({ 'id': self.id })

	@staticmethod
	def VerifyAuthToken(token):
		print("Verificando token...")
		s = Serializer('hola')
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = User.query.get(data['id'])
		return user
