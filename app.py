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
from models.share import Share
from models.securityQuestion import SecurityQuestion
from models.additionalQuestion import AdditionalQuestion
from datetime import date

from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import logging

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct

class SetEncoder(JSONEncoder):
	def default(self, obj):
		try:
			if isinstance(obj, set):
				return list(obj)
		except TypeError:
			pass
		return JSONEncoder.default(self, obj)

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
	app.config.from_object(configFilename)
	app.json_encoder = PythonObjectEncoder
	logging.basicConfig(filename='errorlog.txt', level=logging.DEBUG)
	CORS(app)
	db.init_app(app)

	if appType == 0:
		from views_client import apiBp
		app.register_blueprint(apiBp, url_prefix='/api')
	else:
		from views_admin import apiBp
		app.register_blueprint(apiBp, url_prefix='/api')

	return app
