from flask import render_template

from . import home_bp


@home_bp.route('/')
def home():  
    return render_template('index.html')

@home_bp.route('/about')
def about():  
    return render_template('about.html')