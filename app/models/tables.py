from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(22), unique=True)
	passwd = db.Column(db.String)
	name = db.Column(db.String)
	profile_image = db.Column(db.String)
	#created_on = db.Column(db.DateTime, server_default=db.func.now())
	#updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
	created_on  = db.Column(db.DateTime,  default=db.func.current_timestamp())
	updated_on = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	session = db.relationship("Session", uselist=False, backref="user")

	def __init__(self, ra, username, passwd, name, email):
		self.id = ra
		self.username = username
		self.passwd = passwd
		self.name = name

	def __repr__(self):
		return '<User %r>' % self.username

class Session(db.Model):
	__tablename__ = "sessions"

	id = db.Column(db.Integer, primary_key=True)
	available = db.Column(db.Boolean)
	FPGA = db.Column(db.String, unique=True)
	Arduino = db.Column(db.String, unique=True)
	Camera = db.Column(db.String, unique=True)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())

	def __init__(self, FPGA, Arduino, Camera):
		self.available = True
		self.FPGA = FPGA
		self.Arduino = Arduino
		self.Camera = Camera
		self.user_id = None

	def __repr__(self):
		return "<Post %r>" % self.id
