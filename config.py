class config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None

class localDev(config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test2.sqlite3"
    SECRET_KEY = "just keep guessing....."
    SECURITY_PASSWORD_SALT = "salty_salty_saltyyyy"
    SECURITY_PASSWORD_HASH = "argon2" 
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TRACKABLE = False
    
    
    CACHE_TYPE = 'RedisCache'
    CACHE_KEY_PREFIX = 'my_prefix'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 4
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_DEBUG = False
    CACHE_REDIS_DEBUG = False

    MAIL_DEBUG = False
    DEBUG = False
    
class production(config):
    SQLALCHEMY_DATABASE_URI = None