from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config["FACEBOOK_OAUTH_CLIENT_ID"] = 'some facebook client ID'
app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = 'some facebook client secret'
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from my_app.auth.views import auth, facebook_blueprint
app.register_blueprint(auth)
app.register_blueprint(facebook_blueprint)


with app.app_context():
    db.create_all()
