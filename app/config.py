class BaseConfig:  # Basic Configurations
    pass


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True

    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'root'


config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}
