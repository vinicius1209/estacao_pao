import os
import datetime
from os.path import join, dirname, realpath
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY='123456'
	SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	JWT_EXPIRATION_DELTA=datetime.timedelta(hours=2)
