from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Importing all models
from models.account import Account
from models.accountType import AccountType
from models.product import Product 
from models.recordStatus import RecordStatus
from models.parameterSettings import ParameterSettings
from models.campaign import Campaign
from models.lead import Lead
from models.loan import Loan
from models.shareType import ShareType
from models.person import Person
from models.prospectiveClient import ProspectiveClient
from models.salesRecord import SalesRecord
from models.client import Client
from models.profile import Profile
from models.currency import Currency
from models.transaction import Transaction
from models.blacklist import Blacklist
from models.user import User
from models.bankAccount import BankAccount
from models.blacklistClassification import BlacklistClassification
from models.securityQuestion import SecurityQuestion

from flask.json import JSONEncoder
from datetime import date

class CustomJSONEncoder(JSONEncoder):
	def default(self, obj):
		try:
			if isinstance(obj, date):
				return obj.isoformat()
			iterable = iter(obj)
		except TypeError:
			pass
		else:
			return list(iterable)
		return JSONEncoder.default(self, obj)

def CreateApp(configFilename, appType):
	app = Flask(__name__)
	app.json_encoder = CustomJSONEncoder
	app.config.from_object(configFilename)
	CORS(app)
	db.init_app(app)

	if appType == 0:
		from views_client import apiBp
		app.register_blueprint(apiBp, url_prefix='/api')
	else:
		from views_admin import apiBp
		app.register_blueprint(apiBp, url_prefix='/api')

	return app
