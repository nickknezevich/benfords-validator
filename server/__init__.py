"""Initialize Flask app."""
import datetime
from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import numpy as np
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import logging

logging.getLogger('flask_cors').level = logging.DEBUG
logging.getLogger('flask').level = logging.DEBUG
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

from .models import User, ValidationEntry
def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
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
        
        #reset everything upon restart. In prod this would be done with migrations, for this example this will work.
        db.drop_all()
        db.create_all()  # Create database tables for our data models

        # seed the example data
        user1 = User(first_name='John', last_name="Smith", username="jsmith", email="email@google.com", password=generate_password_hash("test1234"))
        user2 = User(first_name='Andrew', last_name="Lincoln", username="alincoln", email="walkingdead@google.com", password=generate_password_hash("test1234"))

        validationEntry1 = ValidationEntry(user_id=1, title='World Population Data', 
            result={"passed_validation": True, "percentages_plot_data": {"1": 29.914529914529915, "2": 15.81196581196581, "3": 14.102564102564102, "4": 8.974358974358974, "5": 11.11111111111111, "6": 8.11965811965812, "7": 3.418803418803419, "8": 4.273504273504273, "9": 4.273504273504273}}
        )

        validationEntry2 = ValidationEntry(user_id=1, title='2009 Census Data', 
            result={
                "passed_validation": False, "percentages_plot_data": {"1": 29.39970267083611, "2": 18.167837186650942, "3": 12.000820218383144, "4": 9.468395960424465, "5": 7.992002870764341, "6": 7.0231199056748865, "7": 5.977341467165633, "8": 5.341672220228636, "9": 4.629107499871841}}
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(validationEntry1)
        db.session.add(validationEntry2)

        db.session.commit()

        return app