from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

import os, threading, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(host=app.config['HOST'], port=app.config['PORT']))

def start_services():
	print("> Starting services...")
	time.sleep(1)
	os.system("sudo killall usbipd")
	os.system("sudo modprobe usbip-core")
	os.system("sudo modprobe usbip-host")
	os.system("sudo modprobe vhci-hcd")
	time.sleep(1)
	os.system("sudo usbipd")

services = threading.Thread(target = start_services)
services.start()

from app.models import tables
from app.controllers import default
