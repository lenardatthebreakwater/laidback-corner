from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'samplesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth_blueprint.login'

from .models import User
@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

from blog.routes import home_blueprint
app.register_blueprint(home_blueprint)

from blog.routes import auth_blueprint
app.register_blueprint(auth_blueprint)

from blog.routes import post_blueprint
app.register_blueprint(post_blueprint)

from blog.routes import user_blueprint
app.register_blueprint(user_blueprint)
