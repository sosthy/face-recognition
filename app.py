from app import create_app, socketio, db

import os

os.environ["APP_CONFIG_FILE"] = os.path.abspath("config/development.py")

application = create_app()

if __name__ == "__main__":
    socketio.run(application, host="0.0.0.0")
