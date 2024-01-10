import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from blog.forms import UpdateAccountForm
from blog import app, db

user_blueprint = Blueprint("user_blueprint", __name__)

@user_blueprint.route('/user/<int:user_id>/account', methods=['GET', 'POST'])
@login_required
def account(user_id):
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
		return redirect(url_for('user_blueprint.account', user_id=user_id))
	elif request.method == 'GET':
		form.username.data = current_user.username
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', form=form, image_file=image_file)
