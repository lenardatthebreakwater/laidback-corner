import os
import secrets
from PIL import Image
from flask import Flask, render_template, flash, redirect, url_for, request, abort
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is already taken')


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
	submit = SubmitField('Login')


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')
	
	
class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
	picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update Account')
	
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is already taken')


@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
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


@app.route('/')
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts, page=page)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		new_user = User(username=username, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		flash(f'Account successfully created for {form.username.data}', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			flash(f'You are now logged in as {user.username}', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login unsuccessful, please check username or password', 'danger')
	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	flash('You have successfully logout', 'danger')
	return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			random_hex = secrets.token_hex(8)
			_, file_extension = os.path.splitext(form.picture.data.filename)
			new_complete_filename = random_hex + file_extension
			file_path = os.path.join(app.root_path, 'static/profile_pics', new_complete_filename)
			image = Image.open(form.picture.data)
			image.thumbnail((500, 500))
			image.save(file_path)
			current_user.image_file = new_complete_filename
			db.session.commit()
		current_user.username = form.username.data
		db.session.commit()
		flash('Your account has been successfully updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', form=form, image_file=image_file)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(new_post)
		db.session.commit()
		flash('Your post has been created', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', form=form)
	
	
@app.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
	return render_template('post.html', image_file=image_file, post=post)
  
  
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data 
		db.session.commit()
		flash('Your post has been successfully updated', 'success')
		return redirect(url_for('post', post_id=post.id))
	form.title.data = post.title
	form.content.data = post.content
	return render_template('update_post.html', form=form, post=post)


@app.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been successfully deleted', 'danger')
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)
