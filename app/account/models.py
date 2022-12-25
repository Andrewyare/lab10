from .. import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(15), unique=False, nullable=True)
	email = db.Column(db.String(40), unique=False, nullable=True)
	image_file = db.Column(db.String(40), unique=False, nullable=False, default = 'default.jpg')
	password = db.Column(db.String(60), unique=False, nullable=False)

	def __repr__(self):
		return f"User('{self.name}', '{self.email}')"

	@property
	def password_hash(self):
		raise AttributeError('Is not readable')

	@password_hash.setter
	def password_hash(self, password_hash):	
		self.password = bcrypt.generate_password_hash(password_hash)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password_hash = password

	def verify_password(self, password_hash):
		return bcrypt.check_password_hash(self.password, password_hash)