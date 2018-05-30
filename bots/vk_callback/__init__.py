from flask import Blueprint

vk_callback = Blueprint('vk_callback', __name__, )

from . import views
