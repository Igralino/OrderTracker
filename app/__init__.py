from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.debug = False

toolbar = DebugToolbarExtension(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager(app)

from business_account import business
from business_client import business_client
from bots.vk_callback import vk_callback
from bots.alice_dialogs import alice_dialogs
from Chat import Chat

app.register_blueprint(business, url_prefix='/business')
app.register_blueprint(business_client, url_prefix='/business_client')
app.register_blueprint(vk_callback, url_prefix='/bots/vk_callback')
app.register_blueprint(alice_dialogs, url_prefix='/bots/alice_dialogs')
app.register_blueprint(Chat, url_prefix='/chat')

from .mock import mock
from . import models, views
