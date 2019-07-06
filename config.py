import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DLMANAGER_FOLDER = "files/"

HOST = '192.168.1.15'
PORT = 5000
SECRET_KEY = 'Hsyu17Azllj)23jzgks'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
