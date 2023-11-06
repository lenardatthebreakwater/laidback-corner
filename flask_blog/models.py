from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f'<User: {self.username}>'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
