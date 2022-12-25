from flask import Blueprint

form_bp = Blueprint('form', __name__, template_folder='templates/form_cabinet')
from . import views