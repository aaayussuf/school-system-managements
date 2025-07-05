from backend.models.notification import Notification
from backend.app import db

def get_user_notifications(user_id, is_read=None, notification_type=None):
    query = Notification.query.filter_by(user_id=user_id)
    
    if is_read is not None:
        query = query.filter_by(is_read=is_read.lower() == 'true')
    if notification_type:
        query = query.filter_by(notification_type=notification_type)
    
    return query.order_by(Notification.created_at.desc()).all()

def get_notification_by_id(notification_id, user_id):
    return Notification.query.filter_by(id=notification_id, user_id=user_id).first()

def mark_notification_as_read(notification_id, user_id):
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if not notification:
        return False
    
    try:
        notification.is_read = True
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error marking notification as read: {e}")
        return False

def create_notification(data):
    try:
        notification = Notification(
            user_id=data['user_id'],
            title=data['title'],
            message=data['message'],
            notification_type=data.get('notification_type', 'general')
        )
        
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        db.session.rollback()
        print(f"Error creating notification: {e}")
        return None