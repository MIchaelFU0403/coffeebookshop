class BaseConfig():
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '&*(&*&%&$%^rfhtgfrte$swe#w#%%$'

def get_database_uri(DATABASE):
    db = DATABASE.get('DB') or 'mysql'
    driver = DATABASE.get('DRIVER') or 'pymysql'
    username = DATABASE.get('USERNAME') or 'root'
    password = DATABASE.get('PASSWORD') or 'root123'
    host = DATABASE.get('HOST') or '127.0.0.1'
    port = DATABASE.get('PORT') or '3306'
    dbname =DATABASE.get('DBNAME') or 'bookcoffee'
    return '{}+{}://{}:{}@{}:{}/{}'.format(db,driver,username,password,host,port,dbname)

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',
        'POST': '3306',
        'DBNAME': 'bookcoffee',
    }

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)


class TestingConfig(BaseConfig):
    DEBUG = True
    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',
        'POST': '3306',
        'DBNAME': 'bookcoffee',
    }

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)

class StagingConfig(BaseConfig):
    DEBUG = True
    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',
        'POST': '3306',
        'DBNAME': 'bookcoffee',
    }

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)



class ProductConfig(BaseConfig):
    DEBUG = True
    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',
        'POST': '3306',
        'DBNAME': 'bookcoffee',
    }

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)

config = {
'develop':DevelopmentConfig,
'testing':TestingConfig,
'staging':StagingConfig,
'product':ProductConfig,
'default':DevelopmentConfig,
}
