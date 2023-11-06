from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from .forms import RegisterForm, LoginForm
from . import db, bcrypt
from .models import User

auth = Blueprint("auth", __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		new_user = User(username=username, password=hashed_password.decode())
		db.session.add(new_user)
		db.session.commit()
		flash(f'Account successfully created for {form.username.data}', 'success')
		return redirect(url_for('auth.login'))
	return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password.encode('utf-8'), form.password.data):
            login_user(user)
            flash(f'You are now logged in as {user.username}', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful, please check username or password', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
	logout_user()
	flash('You have successfully logout', 'danger')
	return redirect(url_for('main.home'))
