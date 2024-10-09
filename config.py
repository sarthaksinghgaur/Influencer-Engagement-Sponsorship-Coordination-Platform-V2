class config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None

class localDev(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test2.sqlite3"
    SECRET_KEY = "just keep guessing....."
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TRACKABLE = True

class production(config):
    SQLALCHEMY_DATABASE_URI = None