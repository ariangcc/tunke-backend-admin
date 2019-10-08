import os


# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
PORT = 9995
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="tunkeadmin", DB_PASS="gatito21", DB_ADDR="3.216.92.218", DB_NAME="tunke")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
PAGINATION_PAGE_SIZE = 5
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
SECRET_KEY = 'antonellachueca'
