from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()
socketio = SocketIO()
bcrypt = Bcrypt()


def create_app():

    from flask_cors import CORS

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # Load the default configuration
    app.config.from_object("config.default")

    # Load the configuration from the instance folder
    app.config.from_pyfile("config.py")

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    app.config.from_envvar("APP_CONFIG_FILE")

    from app.models import User

    # Init application database
    db.init_app(app)

    # Create all models tables
    db.create_all(app=app)

    # Init Bcrypt
    bcrypt.init_app(app=app)

    login_manager = LoginManager()
    login_manager.login_view = "admin.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_date_for_all_templates():
        return dict(date=datetime.datetime.now())

    from .blueprints import public, admin

    app.register_blueprint(admin.admin, url_prefix="/admin")
    app.register_blueprint(public.public)

    # Init SocketIO
    socketio.init_app(app, async_mode="eventlet", cors_allowed_origins="*")

    return app
