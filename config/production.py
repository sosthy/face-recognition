DEBUG = False  # Turns on debugging features in Flask
BCRYPT_LOG_ROUNDS = 12  # Configuration for the Flask-Bcrypt extension
MAIL_FROM_EMAIL = "sosthenegolden@gmail.com"  # For use in application emails
SQLALCHEMY_ECHO = False
ENV = "production"
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False