
from app import app, db, login_manager
from flask import render_template, flash, request, redirect, session, url_for
from flask_login import login_user, logout_user, login_required, fresh_login_required, current_user
from urlparse import urlparse, urljoin
from werkzeug.security import check_password_hash

from app.models.tables import User
from app.models.forms import LoginForm

def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

login_manager.login_view = "login"
login_manager.login_message = "You must login first in order to see this page contents.&warning"

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(id=user_id).first()

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()

	if request.method == 'POST':
		session['next'] = request.args.get('next')
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.username.data).first()
			user_err = False

			if not user:
				flash("There is no user with that username into our records.&warning")
				user_err = True

			if not user_err and not check_password_hash(user.passwd, form.password.data):
				flash("Password mismatch !&warning")
				user_err = True

			if not user_err:
				login_user(user, remember=form.save.data)
				flash("Welcome back %s !&success" % user.name)

				if 'next' in session and session['next'] and is_safe_url(session['next']):
					return redirect(session['next'])

				return redirect("home")

	return render_template("login.html", form = form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged out !&success")
	return redirect("/")
