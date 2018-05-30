from flask import Blueprint

Chat = Blueprint('Chat', __name__, template_folder='templates')

from . import views
