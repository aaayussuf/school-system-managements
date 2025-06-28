from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import authenticate_user, get_user_profile
from utils.response_utils import make_response
from utils.auth_utils import roles_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return make_response('error', 'Username and password are required', 400)
    
    user = authenticate_user(username, password)
    if not user:
        return make_response('error', 'Invalid credentials', 401)
    
    access_token = create_access_token(identity={
        'id': user.id,
        'username': user.username,
        'role': user.role
    })
    
    return make_response('success', 'Login successful', 200, {
        'access_token': access_token,
        'user': user.to_dict()
    })

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = get_user_profile(current_user['id'])
    
    if not user:
        return make_response('error', 'User not found', 404)
    
    return make_response('success', 'User profile retrieved', 200, user.to_dict())

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
@roles_required('admin')
def protected():
    return make_response('success', 'Protected route accessed', 200)