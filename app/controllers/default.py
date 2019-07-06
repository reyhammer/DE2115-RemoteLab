from app import app, db, login_manager
from app.controllers.login import login_required, fresh_login_required
from flask import render_template, flash, request, redirect

import os.path
from flask import current_app, send_from_directory

@app.context_processor
def inject_user():
    return dict(default_user_profile_image="https://d2p222bhj5cec2.cloudfront.net/attachments/9713176417fef2712fb2850e529e411e9ef5bb3b/store/0c93ec06053c33b105aa1241c6caffc9699ccd3b543d10e10c3c356f6f57/profile_image")

@app.route("/", defaults={'user':None})
@app.route("/index/<user>")
def index(user):
	return render_template("index.html", user = user)

from app.models.tables import User

@app.route("/home")
@login_required
def home():
	return render_template("home.html")

@app.route("/test", defaults={'info': None})
@app.route("/test/<info>")
def test(info):
	i = User(114291, "joao.bruno", "123", "Joao Pedro Ballerini Bruno", "jpedrobruno@hotmail.com")
	db.session.add(i)
	db.session.commit()
	return "Sucesso !!!"

@app.route("/dlmanager/<path:filename>")
def dlmanager(filename):
    uploads = os.path.join(current_app.root_path, app.config['DLMANAGER_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@app.route("/users", methods=["GET"])
def users():
	u = User.query.all()
	for i in u:
		print(i.name, i.created_on, i.updated_on)
	return "OK !"

#@app.route("/test", defaults={'name': None})
#@app.route("/test/<int:value>")
#@app.route("/test")
#@app.route("/test/<name>")
#def test(name=None):
#	if name:
#		return "Hello, %s!" % name
#	else:
#		return "Hello, user !"
