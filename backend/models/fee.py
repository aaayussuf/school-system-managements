from datetime import datetime
from .. import db

class Fee(db.Model):
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # paid, unpaid, partial
    payment_method = db.Column(db.String(50))
    receipt_number = db.Column(db.String(50), unique=True)
    academic_term = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', back_populates='fees')
    
    def __repr__(self):
        return f'<Fee {self.receipt_number} - {self.student.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'student_class': self.student.class_grade if self.student else None,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'payment_method': self.payment_method,
            'receipt_number': self.receipt_number,
            'academic_term': self.academic_term,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }