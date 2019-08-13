from webargs.flaskparser import FlaskParser
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

jwt = JWTManager()
parser = FlaskParser()
client = PyMongo()