from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import datetime

db = SQLAlchemy()
socketio = SocketIO()


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_object("config.default")

    # Load the configuration from the instance folder
    app.config.from_pyfile("config.py")

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    app.config.from_envvar("APP_CONFIG_FILE")

    # Init application database
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "admin.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_date_for_all_templates():
        return dict(date=datetime.datetime.now())

    from .blueprints import admin, public

    app.register_blueprint(admin.admin, url_prefix="/admin")
    app.register_blueprint(public.public)

    # Init SocketIO
    socketio.init_app(app, async_mode="threading")

    return app
