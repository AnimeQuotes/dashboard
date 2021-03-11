import os


class Config:
    ENV = os.environ.get("ENV", "production")
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    PREFERRED_URL_SCHEME = "https"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"


def get_config():
    env = os.environ.get("ENV")
    if env == "development":
        return DevelopmentConfig
    else:
        return ProductionConfig
