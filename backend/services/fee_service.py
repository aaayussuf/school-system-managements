from backend.models.fee import Fee
from backend.models.student import Student
from backend.app import db
from datetime import datetime, date
from sqlalchemy import func, case

def get_all_fees(student_id=None, class_grade=None, status=None, term=None):
    query = Fee.query.join(Student)
    
    if student_id:
        query = query.filter(Fee.student_id == student_id)
    if class_grade:
        query = query.filter(Student.class_grade == class_grade)
    if status:
        query = query.filter(Fee.status == status)
    if term:
        query = query.filter(Fee.academic_term == term)
    
    return query.order_by(Fee.payment_date.desc()).all()

def get_fee_by_id(fee_id):
    return Fee.query.get(fee_id)

def create_fee(data):
    try:
        fee = Fee(
            student_id=data['student_id'],
            amount=data['amount'],
            payment_date=datetime.strptime(data['payment_date'], '%Y-%m-%d').date() if data.get('payment_date') else None,
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
            status=data['status'],
            payment_method=data.get('payment_method'),
            receipt_number=data['receipt_number'],
            academic_term=data['academic_term'],
            description=data.get('description', '')
        )
        
        db.session.add(fee)
        db.session.commit()
        return fee
    except Exception as e:
        db.session.rollback()
        print(f"Error creating fee: {e}")
        return None

def update_fee(fee_id, data):
    fee = Fee.query.get(fee_id)
    if not fee:
        return None
    
    try:
        if 'amount' in data:
            fee.amount = data['amount']
        if 'payment_date' in data:
            fee.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date() if data['payment_date'] else None
        if 'due_date' in data:
            fee.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        if 'status' in data:
            fee.status = data['status']
        if 'payment_method' in data:
            fee.payment_method = data['payment_method']
        if 'receipt_number' in data:
            fee.receipt_number = data['receipt_number']
        if 'academic_term' in data:
            fee.academic_term = data['academic_term']
        if 'description' in data:
            fee.description = data['description']
        
        db.session.commit()
        return fee
    except Exception as e:
        db.session.rollback()
        print(f"Error updating fee: {e}")
        return None

def delete_fee(fee_id):
    fee = Fee.query.get(fee_id)
    if not fee:
        return False
    
    try:
        db.session.delete(fee)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting fee: {e}")
        return False

def get_fee_summary():
    # Total fees collected
    total_paid = db.session.query(func.sum(Fee.amount)).filter(Fee.status == 'paid').scalar() or 0
    
    # Outstanding dues
    outstanding = db.session.query(func.sum(Fee.amount)).filter(Fee.status.in_(['unpaid', 'partial'])).scalar() or 0
    
    # Class-wise summary
    class_summary = db.session.query(
        Student.class_grade,
        func.sum(Fee.amount).label('total_amount'),
        func.sum(case([(Fee.status == 'paid', Fee.amount)], else_=0)).label('paid_amount'),
        func.sum(case([(Fee.status.in_(['unpaid', 'partial']), Fee.amount)], else_=0)).label('outstanding_amount')
    ).join(Student).group_by(Student.class_grade).all()
    
    return {
        'total_paid': float(total_paid),
        'outstanding_dues': float(outstanding),
        'class_summary': [
            {
                'class_grade': item.class_grade,
                'total_amount': float(item.total_amount),
                'paid_amount': float(item.paid_amount),
                'outstanding_amount': float(item.outstanding_amount)
            } for item in class_summary
        ]
    }
