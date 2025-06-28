from datetime import time
from .. import db

class Timetable(db.Model):
    __tablename__ = 'timetable'
    
    id = db.Column(db.Integer, primary_key=True)
    class_grade = db.Column(db.String(32), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # Monday, Tuesday, etc.
    period_number = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    academic_term = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Timetable {self.class_grade} - {self.day_of_week} - Period {self.period_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'class_grade': self.class_grade,
            'day_of_week': self.day_of_week,
            'period_number': self.period_number,
            'subject': self.subject,
            'teacher_id': self.teacher_id,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'academic_term': self.academic_term
        }