import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///atlas_hydro.db")
    SQLALCHEMY_ENGINE_OPTIONS = (
        {
            "connect_args": {
                "timeout": 30,
            },
        }
        if SQLALCHEMY_DATABASE_URI.startswith("sqlite")
        else {}
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Variables valables seulement en développement
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL")

    DEBUG = os.getenv("FLASK_ENV", "development") != "production"
