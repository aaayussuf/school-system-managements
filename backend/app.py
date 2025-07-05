from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import config
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.students import students_bp
    from .routes.fees import fees_bp
    from .routes.attendance import attendance_bp
    from .routes.timetable import timetable_bp
    from .routes.notifications import notifications_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(fees_bp, url_prefix='/api/fees')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(timetable_bp, url_prefix='/api/timetable')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    
    @app.route('/')
    def index():
        return {'message': 'School Management System Backend is Live!'}
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
