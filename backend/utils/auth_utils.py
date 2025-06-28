from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def roles_required(*required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') in required_roles:
                return fn(*args, **kwargs)
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Insufficient permissions',
                    'data': None
                }), 403
        return decorator
    return wrapper