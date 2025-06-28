from models.attendance import Attendance
from models.student import Student
from app import db
from datetime import datetime, date
from sqlalchemy import func, case

def get_attendance_records(student_id=None, class_grade=None, date_from=None, date_to=None):
    query = Attendance.query.join(Student)
    
    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    if class_grade:
        query = query.filter(Student.class_grade == class_grade)
    if date_from:
        query = query.filter(Attendance.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        query = query.filter(Attendance.date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    return query.order_by(Attendance.date.desc()).all()

def get_attendance_by_id(attendance_id):
    return Attendance.query.get(attendance_id)

def mark_attendance(data):
    try:
        attendance = Attendance(
            student_id=data['student_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            status=data['status'],
            remarks=data.get('remarks', ''),
            recorded_by=data['recorded_by']
        )
        
        db.session.add(attendance)
        db.session.commit()
        return attendance
    except Exception as e:
        db.session.rollback()
        print(f"Error creating attendance: {e}")
        return None

def update_attendance(attendance_id, data):
    attendance = Attendance.query.get(attendance_id)
    if not attendance:
        return None
    
    try:
        if 'date' in data:
            attendance.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'status' in data:
            attendance.status = data['status']
        if 'remarks' in data:
            attendance.remarks = data['remarks']
        if 'recorded_by' in data:
            attendance.recorded_by = data['recorded_by']
        
        db.session.commit()
        return attendance
    except Exception as e:
        db.session.rollback()
        print(f"Error updating attendance: {e}")
        return None

def delete_attendance(attendance_id):
    attendance = Attendance.query.get(attendance_id)
    if not attendance:
        return False
    
    try:
        db.session.delete(attendance)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting attendance: {e}")
        return False

def get_attendance_summary(class_grade=None, date_from=None, date_to=None):
    query = db.session.query(
        Student.class_grade,
        func.count(Attendance.id).label('total_records'),
        func.sum(case([(Attendance.status == 'present', 1)], else_=0)).label('present_count'),
        func.sum(case([(Attendance.status == 'absent', 1)], else_=0)).label('absent_count'),
        func.sum(case([(Attendance.status == 'late', 1)], else_=0)).label('late_count'),
        func.sum(case([(Attendance.status == 'excused', 1)], else_=0)).label('excused_count')
    ).join(Student)
    
    if class_grade:
        query = query.filter(Student.class_grade == class_grade)
    if date_from:
        query = query.filter(Attendance.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        query = query.filter(Attendance.date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    query = query.group_by(Student.class_grade)
    results = query.all()
    
    summary = []
    for result in results:
        summary.append({
            'class_grade': result.class_grade,
            'total_records': result.total_records,
            'present_count': result.present_count,
            'absent_count': result.absent_count,
            'late_count': result.late_count,
            'excused_count': result.excused_count,
            'attendance_rate': round((result.present_count / result.total_records) * 100, 2) if result.total_records > 0 else 0
        })
    
    return summary