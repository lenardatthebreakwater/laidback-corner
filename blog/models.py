from . import db
from flask_login import UserMixin
from datetime import datetime

user_post = db.Table(
	'user_post',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	posts = db.relationship('Post', backref='author', lazy=True)
	liked_posts = db.relationship('Post', secondary=user_post, backref='likers')

	def __repr__(self):
		return f'<User: {self.username}>'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	likes = db.Column(db.Integer, nullable=False, default=0)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f'<Post: {self.title}>'
