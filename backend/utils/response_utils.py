from flask import jsonify

def make_response(status, message, code, data=None):
    response = {
        'status': status,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code