class config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None

class localDev(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test2.sqlite3"
    SECRET_KEY = "just keep guessing....."
    SECURITY_PASSWORD_SALT = "salty_salty_saltyyyy"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = "argon2" 
    
class production(config):
    SQLALCHEMY_DATABASE_URI = None