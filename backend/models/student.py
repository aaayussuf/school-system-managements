from datetime import datetime
from .. import db

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    full_name = db.Column(db.String(128), nullable=False)
    student_id = db.Column(db.String(32), unique=True, nullable=False)
    photo_path = db.Column(db.String(256))
    class_grade = db.Column(db.String(32), nullable=False)
    guardian_name = db.Column(db.String(128), nullable=False)
    guardian_relation = db.Column(db.String(64), nullable=False)
    address = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='student')
    fees = db.relationship('Fee', back_populates='student')
    attendances = db.relationship('Attendance', back_populates='student')
    
    def __repr__(self):
        return f'<Student {self.student_id} - {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'student_id': self.student_id,
            'photo_path': self.photo_path,
            'class_grade': self.class_grade,
            'guardian_name': self.guardian_name,
            'guardian_relation': self.guardian_relation,
            'address': self.address,
            'contact_number': self.contact_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }