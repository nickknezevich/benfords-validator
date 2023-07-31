from flask import Flask
from flask import request, jsonify, abort
import time

def api_response_error(status_code, errors):
    response = jsonify({
        'version': '1.0',
        'status': status_code,
        'errors': errors
    })
    response.status_code = status_code
    return response

def api_response_success(data, start_time):

    response_time = time.time() - start_time

    response_time_in_ms = '{:.2f}ms'.format(response_time*1000)
    response = jsonify({
            'version': '1.0',
            'code': 200,
            'response_time': response_time_in_ms,
            'message': 'success',
            'data': data
    })
    response.status_code = 200
    return response