from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import config 

app = Flask(__name__)
app.config.from_object(config.Config) 

# Sql Alchemy / Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes

def execute_app():
    return app