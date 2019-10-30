from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from flask import g
from models.user import User
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()

@auth.verify_password
def VerifyPassword(emailOrToken, password):
	# first try to authenticate by token
	user = User.VerifyAuthToken(emailOrToken)
	if user:
		print("Token valido!")
	if not user:
		# try to authenticate with email/password
		print("Token invalido, chekeando password")
		user = User.query.filter_by(email=emailOrToken).first()
		if not user or not check_password_hash(user.password, password):
			return False
	
	g.user = user
	return True

class AuthRequiredResource(Resource):
	method_decorators = [auth.login_required]