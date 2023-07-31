"""Initialize Flask app."""
import json
import os
import sys
import time
from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request
from werkzeug.utils import secure_filename
import numpy as np
from flask_restful import Resource, Api, reqparse
import werkzeug
import pandas as pd
from benfordslaw import benfordslaw
from flask_cors import CORS
import logging
logging.getLogger('flask_cors').level = logging.DEBUG
logging.getLogger('flask').level = logging.DEBUG
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    #auth = HTTPTokenAuth(scheme='Bearer')
    app = Flask(__name__)
    app.json.sort_keys = False
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bv:test1234@bv.mysql:3306/bv' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    CORS(app)
    #app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from . import models  
        from . import routes  # Import routes
        
        #reset everything. In prod this would be done in a different way
        #db.drop_all()
        db.create_all()  # Create database tables for our data models
        db.session.commit()

        return app