from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from blog.forms import PostForm, UpdatePostForm
from blog.models import Post
from blog import db

post_blueprint = Blueprint("post_blueprint", __name__)

@post_blueprint.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(new_post)
		db.session.commit()
		flash('Your post has been created', 'success')
		return redirect(url_for('home_blueprint.home'))
	return render_template('create_post.html', title="New Post", form=form)

@post_blueprint.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
	return render_template('post.html', title="Post", image_file=image_file, post=post)
  
@post_blueprint.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = UpdatePostForm()
	if form.validate_on_submit():
		try:
			post.title = form.title.data
			post.content = form.content.data 
			db.session.commit()
			flash('Your post has been successfully updated', 'success')
		except:
			db.session.rollback()
			flash('You already have a post with the same name')
		return redirect(url_for('post_blueprint.post', post_id=post.id))
	form.title.data = post.title
	form.content.data = post.content
	return render_template('update_post.html', title="Update Post", form=form, post=post)

@post_blueprint.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been successfully deleted', 'danger')
	return redirect(url_for('home_blueprint.home'))
