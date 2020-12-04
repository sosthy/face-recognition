DEBUG = True  # Turns on debugging features in Flask
SQLALCHEMY_ECHO = True
ENV = "development"
# SQLALCHEMY_DATABASE_URI= "postgresql://postgres:postgres@localhost/face-recognition"
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False
