from flask import Blueprint, request, render_template
from blog.models import Post
from blog import db

home_blueprint = Blueprint("home_blueprint", __name__)

@home_blueprint.route("/")
@home_blueprint.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts, page=page)
