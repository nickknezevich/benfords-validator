from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, ValidationError
import json
from flask import current_app as app, g, jsonify
from flask import make_response, redirect, render_template, request, url_for
from flask_httpauth import HTTPTokenAuth
import time
from werkzeug.utils import secure_filename
import pandas as pd
from .api_response import api_response_error, api_response_success
from benfordslaw import benfordslaw
from .models import User, ValidationEntry, db
import logging
logging.getLogger('flask_cors').level = logging.DEBUG

# Base Marschallow Seralized Schemas
class Login(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class BaseUser(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    picture = fields.String(required=False)
    created_at = fields.String(required=False)
    updated_at = fields.String(required=False)

class SerializedUser(Schema):
    id=fields.String(required=True)
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    picture = fields.String(required=False)
    created_at = fields.String(required=False)
    updated_at = fields.String(required=False)

class BaseValidationEntry(Schema):
    id = fields.String(required=True)
    user_id = fields.String(required=False)
    title = fields.String(required=True)
    result = fields.Dict(required=True)
    created_at = fields.String(required=False)
    updated_at = fields.String(required=False)

class SerializedValidationEntry(Schema):
    id = fields.String(required=True)
    user = fields.Nested(SerializedUser())
    title = fields.String(required=True)
    result = fields.Dict(required=True)
    created_at = fields.String(required=False)
    updated_at = fields.String(required=False)

class ValidationEntryRequest(Schema):
    title = fields.String(required=True)
    file = fields.Raw(type='file')
    reference_column = fields.String(required=True)
    separator=fields.String(required=False)

auth = HTTPTokenAuth(scheme='Bearer')

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xls', 'xlsx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/hc')
def hc():
    return {'status': 'ok'}


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    app.logger.debug(user)
    if not user:
        return False
    g.user = user
    return True


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/auth/login', methods=['POST'])
def login():
    start_time = time.time()
    request_data = request.json
    schema = Login()

    try:
        result = schema.load(request_data)
        username = request_data.get('username')
        password = request_data.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return api_response_error(401, {"auth": "failed"})
        g.user = user
        token = user.generate_auth_token(600000)
        schema = BaseUser()
        res = {
            'token': token.decode('ascii'),
            'user': schema.dump(user)
        }
        return api_response_success(res, start_time)
    except ValidationError as err:
        return api_response_error(400, err.messages)


@auth.login_required
def get_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/file-upload', methods=['POST'])
@auth.login_required
def upload_file():
    try:
        start_time = time.time()
        request_data = request.form
        schema = ValidationEntryRequest()

        schema.load(request_data)
        title = request_data.get('title')
        separator = request_data.get('separator')
        
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
            df = pd.read_csv(request.files.get('file'),
                                 sep=separator, usecols=[reference_column], skipinitialspace=True)
            df.iloc[1:]
            bl = benfordslaw(alpha=0.05)
            validation_result = bl.fit(df)
            app.logger.debug(validation_result)
            passed_validation = True if validation_result['P_significant'] == False else False
            data_dict = {str(int(item[0])): item[1]
                         for item in validation_result['percentage_emp'].tolist()}
            response_data = {
                'passed_validation': passed_validation,
                'percentages_plot_data': data_dict
            }
            res = save_result(title,response_data)
            
            return api_response_success({
                'user_id': g.user.id,
                'user': {
                    'first_name': g.user.first_name,
                    'last_name': g.user.last_name,
                    'email': g.user.email,
                    'picture': g.user.picture
                },
                'title': title,
                'result': {
                    'passed_validation': passed_validation,
                    'percentages_plot_data': data_dict,
                },
                'created_at': res.created_at,
                'updated_at': res.updated_at
            }, start_time)
        else:
            return api_response_error(400, {'file': 'Allowed file types are txt, csv, xls, xlsx'})
    except ValidationError as err:
        return api_response_error(400, err.messages)
    except Exception as e:
        app.logger.error(e)
        return api_response_error(500, {'message': 'There was a problem while parsing the file'})

@app.route('/api/users', methods=['GET'])
@auth.login_required
def get_users():
    try:
        start_time = time.time()
        schema = BaseUser(many=True)
        users = User.query.all()
        serialized_data = schema.dump(users)
        return api_response_success(serialized_data, start_time)
    except Exception as e:
        app.logger.error(e)
        return api_response_error(500, {'message': 'There was a problem while retrieving the Users'})


@app.route('/api/users', methods=['POST'])
def add_user():
    start_time = time.time()
    request_data = request.json
    schema = BaseUser()

    try:
        result = schema.load(request_data)
        username = request_data.get('username')
        password = request_data.get('password')
        picture = request_data.get('picture')
        first_name = request_data.get('first_name')
        last_name = request_data.get('last_name')
        email = request_data.get('email')

        # Create and persist the user
        user = User(username=username, password=generate_password_hash(password), first_name=first_name,
                    last_name=last_name, picture=picture, email=email)
        db.session.add(user)
        db.session.commit()

        return api_response_success(result, start_time)
    except ValidationError as err:
        return api_response_error(400, err.messages)

@app.route('/api/validation-entries', methods=['GET'])
@auth.login_required
def get_validation_entries():
    try:
        start_time = time.time()
        schema = SerializedValidationEntry(many=True)
        entries = ValidationEntry.query.filter(ValidationEntry.user_id == g.user.id).order_by(ValidationEntry.created_at.desc())
        serialized_data = schema.dump(entries)
        return api_response_success(serialized_data, start_time)
    except Exception as e:
        app.logger.error(e)
        return api_response_error(500, {'message': 'There was a problem while retrieving the Validation Entries'})

def save_result(title, result):
    try:
        entry = ValidationEntry(user_id=g.user.id, title=title,
                                result=result)
        db.session.add(entry)
        db.session.commit()
        return entry
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
