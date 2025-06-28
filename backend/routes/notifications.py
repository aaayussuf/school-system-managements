from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.notification_service import (
    get_user_notifications,
    get_notification_by_id,
    mark_notification_as_read,
    create_notification
)
from utils.response_utils import make_response

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def list_notifications():
    user_id = get_jwt_identity()['id']
    is_read = request.args.get('is_read')
    notification_type = request.args.get('type')
    
    notifications = get_user_notifications(user_id, is_read, notification_type)
    return make_response('success', 'Notifications retrieved', 200, [n.to_dict() for n in notifications])

@notifications_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    user_id = get_jwt_identity()['id']
    notification = get_notification_by_id(notification_id, user_id)
    if not notification:
        return make_response('error', 'Notification not found', 404)
    return make_response('success', 'Notification retrieved', 200, notification.to_dict())

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    user_id = get_jwt_identity()['id']
    success = mark_notification_as_read(notification_id, user_id)
    if not success:
        return make_response('error', 'Notification not found', 404)
    return make_response('success', 'Notification marked as read', 200)

@notifications_bp.route('/', methods=['POST'])
@jwt_required()
def add_notification():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    # Only allow admin to send notifications to other users
    if current_user['role'] != 'admin' and data.get('user_id') != current_user['id']:
        return make_response('error', 'Unauthorized to create notifications for others', 403)
    
    notification = create_notification(data)
    if not notification:
        return make_response('error', 'Failed to create notification', 400)
    return make_response('success', 'Notification created', 201, notification.to_dict())