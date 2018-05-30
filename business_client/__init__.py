from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy

business_client = Blueprint('business_client', __name__, template_folder='templates', static_folder='../business/static')
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from . import views
