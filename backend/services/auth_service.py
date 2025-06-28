from models.user import User
from app import db

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password) and user.is_active:
        return user
    return None

def get_user_profile(user_id):
    return User.query.get(user_id)

def create_user(username, email, password, role):
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return None
    
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return user