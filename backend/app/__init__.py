from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from . import config 

app = Flask(__name__)
app.config.from_object(config.Config) 

# Cors
CORS(app)

# Sql Alchemy / Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .auth import authenticate, identity

jwt = JWT(app, authenticate, identity)

from app import routes

def execute_app():
    return app