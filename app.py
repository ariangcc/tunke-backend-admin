from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Importing all models
from models.prospectiveclient import ProspectiveClient
from models.client import Client
from models.profile import Profile
from models.currency import Currency
from models.transaction import Transaction
from models.blacklist import Blacklist
from models.blacklist_clasification import Blacklist_clasification

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

def create_app(config_filename, app_type):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(config_filename)
    CORS(app)
    db.init_app(app)

    if app_type == 0:
        from views_client import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
    else:
        from views_admin import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')

    return app
