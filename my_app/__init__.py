from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config["FACEBOOK_OAUTH_CLIENT_ID"] = 'some facebook client ID'
app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = 'some facebook client secret'
app.config["GOOGLE_OAUTH_CLIENT_ID"] = "my google oauth client ID"
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "my google oauth client secret"
app.config["OAUTHLIB_RELAX_TOKEN_SCOPE"] = True
app.config["TWITTER_OAUTH_CLIENT_KEY"] = "twitter app api key"
app.config["TWITTER_OAUTH_CLIENT_SECRET"] = "twitter app secret key"
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from my_app.auth.views import auth, facebook_blueprint, google_blueprint, twitter_blueprint
app.register_blueprint(auth)
app.register_blueprint(facebook_blueprint)
app.register_blueprint(google_blueprint)
app.register_blueprint(twitter_blueprint)


db.create_all()
