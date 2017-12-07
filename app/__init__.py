from flask import Flask
from flask-sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config_from_object(config[config_name])
    config[config_name].init_app(app)
    db.init(app)

    return app
