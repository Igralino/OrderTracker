from flask import Blueprint
from flask import Flask

business = Blueprint('business', __name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = '/business_account/static/images'
ALLOWED_EXTENSIONS = {'jpg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from . import views
