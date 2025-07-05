from backend.models.timetable import Timetable
from backend.app import db

def get_timetable_entries(class_grade=None, teacher_id=None, day=None, term=None):
    query = Timetable.query
    
    if class_grade:
        query = query.filter_by(class_grade=class_grade)
    if teacher_id:
        query = query.filter_by(teacher_id=teacher_id)
    if day:
        query = query.filter_by(day_of_week=day)
    if term:
        query = query.filter_by(academic_term=term)
    
    return query.order_by(Timetable.period_number).all()

def get_timetable_by_id(timetable_id):
    return Timetable.query.get(timetable_id)

def create_timetable_entry(data):
    try:
        entry = Timetable(
            class_grade=data['class_grade'],
            day_of_week=data['day_of_week'],
            period_number=data['period_number'],
            subject=data['subject'],
            teacher_id=data.get('teacher_id'),
            start_time=data['start_time'],
            end_time=data['end_time'],
            academic_term=data['academic_term']
        )
        
        db.session.add(entry)
        db.session.commit()
        return entry
    except Exception as e:
        db.session.rollback()
        print(f"Error creating timetable entry: {e}")
        return None

def update_timetable_entry(timetable_id, data):
    entry = Timetable.query.get(timetable_id)
    if not entry:
        return None
    
    try:
        entry.class_grade = data.get('class_grade', entry.class_grade)
        entry.day_of_week = data.get('day_of_week', entry.day_of_week)
        entry.period_number = data.get('period_number', entry.period_number)
        entry.subject = data.get('subject', entry.subject)
        entry.teacher_id = data.get('teacher_id', entry.teacher_id)
        entry.start_time = data.get('start_time', entry.start_time)
        entry.end_time = data.get('end_time', entry.end_time)
        entry.academic_term = data.get('academic_term', entry.academic_term)
        
        db.session.commit()
        return entry
    except Exception as e:
        db.session.rollback()
        print(f"Error updating timetable entry: {e}")
        return None

def delete_timetable_entry(timetable_id):
    entry = Timetable.query.get(timetable_id)
    if not entry:
        return False
    
    try:
        db.session.delete(entry)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting timetable entry: {e}")
        return False