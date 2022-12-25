from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from config import config


bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message_category = 'info'

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name = 'default'):
	app = Flask(__name__)
    # setup with the configuration provided by the user / environment
	app.config.from_object(config.get(config_name))
    # setup all our dependencies
	db.init_app(app)
	migrate.init_app(app, db, render_as_batch=True)
	bcrypt.init_app(app)
	login_manager.init_app(app)
    
	with app.app_context():
		from app.home import home_bp
		from app.form_cabinet import form_bp
		from app.account import account_bp
		from app.todo import todo_bp
		
		app.register_blueprint(home_bp)
		app.register_blueprint(form_bp)
		app.register_blueprint(account_bp)
		app.register_blueprint(todo_bp)
        
	return app