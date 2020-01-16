import os

class Config:
    pass
    """
    the main parent class
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:kent1234@localhost/pitches'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    #email_config
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_PORT=608

class ProdConfig(Config):
    """
    inherites from the parent class and used to run the application during production
    """
    SQLALCHEMY_DATABASE_URI = os.environ("DATABASE_URL")

class DevConfig(Config):

    DEBUG =  True
    SECRET_KEY='f6c2e27f1d8496ac9a05f7dae0ff2ccd'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:kent1234@localhost/pitches'
    ENV='development'

config_options= {
'development':DevConfig,
'production':ProdConfig
}