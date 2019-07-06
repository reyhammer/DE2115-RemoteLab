from app import app, db, login_manager
from flask import render_template, flash, request, redirect, session, url_for
from werkzeug.security import generate_password_hash
from app.models.forms import RegisterForm

from app.models.tables import User

@app.route("/register", methods=["GET", "POST"])
def register():
  form = RegisterForm()

  if request.method == 'POST':
    if form.validate_on_submit():
      i = User(form.ra.data, form.username.data, generate_password_hash(form.password.data, method='sha256'), form.name.data+" "+form.surname.data, form.email.data)
      db.session.add(i)

      try:
        db.session.commit()
      except Exception as err:
        db.session.rollback()
        flash("This user already exists.&warning")
        return redirect("register")

      return redirect("login")
  return render_template("register.html", form = form)
