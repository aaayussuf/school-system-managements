from backend.models.student import Student
from backend.models.fee import Fee
from backend.models.attendance import Attendance
from app import db
from datetime import datetime, date
from sqlalchemy import func
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
from config import Config

def generate_report_card(student_id, term):
    # Get student data
    student = Student.query.get(student_id)
    if not student:
        return None
    
    # Get attendance summary for the term
    attendance_summary = db.session.query(
        func.count(Attendance.id).label('total_days'),
        func.sum(case([(Attendance.status == 'present', 1)], else_=0)).label('present_days')
    ).filter(
        Attendance.student_id == student_id,
        Attendance.date >= date(2023, 1, 1),  # Adjust based on term
        Attendance.date <= date(2023, 12, 31)   # Adjust based on term
    ).first()
    
    # Get fee status for the term
    fee_status = Fee.query.filter_by(
        student_id=student_id,
        academic_term=term
    ).first()
    
    # Prepare data for template
    report_data = {
        'student': student.to_dict(),
        'term': term,
        'current_date': datetime.now().strftime('%Y-%m-%d'),
        'attendance': {
            'total_days': attendance_summary.total_days if attendance_summary else 0,
            'present_days': attendance_summary.present_days if attendance_summary else 0,
            'attendance_rate': round((attendance_summary.present_days / attendance_summary.total_days) * 100, 2) if attendance_summary and attendance_summary.total_days > 0 else 0
        },
        'fee_status': fee_status.status if fee_status else 'Not Available'
    }
    
    # Render HTML template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_card.html')
    html_content = template.render(report_data)
    
    # Ensure output directory exists
    output_dir = os.path.join(Config.UPLOAD_FOLDER, 'reports')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate PDF
    output_path = os.path.join(output_dir, f'report_card_{student_id}_{term}.pdf')
    pdfkit.from_string(html_content, output_path)
    
    return output_path