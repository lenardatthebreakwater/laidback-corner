from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .forms import PostForm
from .models import Post
from . import db

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
		return redirect(url_for('main_blueprint.home'))
	return render_template('create_post.html', form=form)

@post_blueprint.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
	return render_template('post.html', image_file=image_file, post=post)
  
@post_blueprint.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
		return redirect(url_for('post_blueprint.post', post_id=post.id))
	form.title.data = post.title
	form.content.data = post.content
	return render_template('update_post.html', form=form, post=post)

@post_blueprint.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been successfully deleted', 'danger')
	return redirect(url_for('main_blueprint.home'))

@post_blueprint.route('/post/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
	post = Post.query.get_or_404(post_id)
	if not current_user.is_authenticated:
		return "You need to login in order to like a post", 401
	if post in current_user.liked_posts:
		current_user.liked_posts.remove(post)
		post.likes -= 1
		db.session.commit()
		return f'{post.likes}'
	current_user.liked_posts.append(post)
	post.likes += 1
	db.session.commit()
	return f'{post.likes}'
