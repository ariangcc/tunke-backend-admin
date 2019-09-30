from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Importing all models
from models.profile import Profile
from models.currency import Currency
from models.transaction import Transaction

def create_app(config_filename, app_type):
    app = Flask(__name__)
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
