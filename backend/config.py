class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///atlas_hydro.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Valable seulement en développement
    CACHE_TYPE = "SimpleCache"

    DEBUG = True
