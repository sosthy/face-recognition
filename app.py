from app import create_app, socketio

import os

os.environ["APP_CONFIG_FILE"] = os.path.abspath("config/production.py")

app = create_app()
socketio.run(app, host="0.0.0.0")

if __name__ == "__main__":
    pass
