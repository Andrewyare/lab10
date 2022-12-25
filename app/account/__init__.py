from flask import Blueprint

account_bp = Blueprint('account', __name__, template_folder='templates/auth')

from . import views