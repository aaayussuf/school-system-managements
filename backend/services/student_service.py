from models.student import Student
from models.user import User
from app import db
from datetime import datetime
import os
from config import Config

def get_all_students(class_grade=None):
    query = Student.query
    if class_grade:
        query = query.filter_by(class_grade=class_grade)
    return query.all()

def get_student_by_id(student_id):
    return Student.query.get(student_id)

def create_student(data):
    try:
        # First create the user account
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            role='student',
            is_active=True
        )
        user.set_password(data.get('password', 'defaultpassword'))
        db.session.add(user)
        db.session.flush()  # To get the user ID
        
        # Then create the student record
        student = Student(
            user_id=user.id,
            full_name=data['full_name'],
            student_id=data['student_id'],
            class_grade=data['class_grade'],
            guardian_name=data['guardian_name'],
            guardian_relation=data['guardian_relation'],
            address=data['address'],
            contact_number=data['contact_number']
        )
        
        db.session.add(student)
        db.session.commit()
        return student
    except Exception as e:
        db.session.rollback()
        print(f"Error creating student: {e}")
        return None

def update_student(student_id, data):
    student = Student.query.get(student_id)
    if not student:
        return None
    
    try:
        student.full_name = data.get('full_name', student.full_name)
        student.class_grade = data.get('class_grade', student.class_grade)
        student.guardian_name = data.get('guardian_name', student.guardian_name)
        student.guardian_relation = data.get('guardian_relation', student.guardian_relation)
        student.address = data.get('address', student.address)
        student.contact_number = data.get('contact_number', student.contact_number)
        
        db.session.commit()
        return student
    except Exception as e:
        db.session.rollback()
        print(f"Error updating student: {e}")
        return None

def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return False
    
    try:
        # Delete associated user
        user = User.query.get(student.user_id)
        if user:
            db.session.delete(user)
        
        db.session.delete(student)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting student: {e}")
        return False