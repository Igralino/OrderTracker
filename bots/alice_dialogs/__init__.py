from flask import Blueprint

alice_dialogs = Blueprint('alice_dialogs', __name__, )

from . import views
