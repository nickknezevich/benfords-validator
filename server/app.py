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
from api_response import api_response_error, api_response_success
import logging
logging.getLogger('flask_cors').level = logging.DEBUG
from flask_sqlalchemy import SQLAlchemy
from models import User, ValidationEntry, db

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xls', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


auth = HTTPTokenAuth(scheme='Bearer')
app = Flask(__name__)
app.json.sort_keys = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bv:test1234@localhost:3311/bv' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

@app.route('/api/hc')
def hello():
    return {'status': 'ok'}


tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.route('/api')
# @auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


@app.route('/api/file-upload', methods=['POST'])
def upload_file():
    try:
        start_time = time.time()
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if request.form.get('reference_column') == None:
            return api_response_error(400, {'referece_column': 'Reference column must not be empty'})
        reference_column = request.form.get('reference_column')
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file = request.files['file']
            try:
                df = pd.read_csv(request.files.get('file'),
                              sep='\t', usecols=[reference_column])
            except Exception as e:
                df = pd.read_csv(request.files.get('file'),
                              usecols=[reference_column], skipinitialspace=True)
            df.iloc[1:]
            bl = benfordslaw(alpha=0.05)
            validation_result = bl.fit(df)
            passed_validation = True if validation_result['P_significant'] == 'False' else False
            data_dict = {str(int(item[0])): item[1]
                         for item in validation_result['percentage_emp'].tolist()}
            response_data = {
                'passed_validation': passed_validation,
                'percentages_plot_data': data_dict
            }
            save_result(response_data)
            return api_response_success(response_data, start_time)
        else:
            return api_response_error(400, {'message': 'Allowed file types are txt, csv'})
    except Exception as e:
        app.logger.error(e)
        return api_response_error(500, {'message': 'There was a problem while parsing the file'})

def save_result(result):
    try:
        entry = ValidationEntry(user='nikola',
                result=json.dumps(result))
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        logging.error(e)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    
