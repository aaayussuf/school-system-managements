from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..services.attendance_service import (
    get_attendance_records,
    get_attendance_by_id,
    mark_attendance,
    update_attendance,
    delete_attendance,
    get_attendance_summary
)
from ..utils.response_utils import make_response
from ..utils.auth_utils import roles_required

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['GET'])
@jwt_required()
def list_attendance():
    student_id = request.args.get('student_id')
    class_grade = request.args.get('class')
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    attendance = get_attendance_records(student_id, class_grade, date_from, date_to)
    return make_response('success', 'Attendance records retrieved', 200, [a.to_dict() for a in attendance])

@attendance_bp.route('/<int:attendance_id>', methods=['GET'])
@jwt_required()
def get_attendance(attendance_id):
    record = get_attendance_by_id(attendance_id)
    if not record:
        return make_response('error', 'Attendance record not found', 404)
    return make_response('success', 'Attendance record retrieved', 200, record.to_dict())

@attendance_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('teacher', 'admin')
def add_attendance():
    data = request.get_json()
    record = mark_attendance(data)
    if not record:
        return make_response('error', 'Failed to create attendance record', 400)
    return make_response('success', 'Attendance recorded', 201, record.to_dict())

@attendance_bp.route('/<int:attendance_id>', methods=['PUT'])
@jwt_required()
@roles_required('teacher', 'admin')
def modify_attendance(attendance_id):
    data = request.get_json()
    record = update_attendance(attendance_id, data)
    if not record:
        return make_response('error', 'Attendance record not found', 404)
    return make_response('success', 'Attendance record updated', 200, record.to_dict())

@attendance_bp.route('/<int:attendance_id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def remove_attendance(attendance_id):
    success = delete_attendance(attendance_id)
    if not success:
        return make_response('error', 'Attendance record not found', 404)
    return make_response('success', 'Attendance record deleted', 200)

@attendance_bp.route('/summary', methods=['GET'])
@jwt_required()
def attendance_summary():
    class_grade = request.args.get('class')
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    summary = get_attendance_summary(class_grade, date_from, date_to)
    return make_response('success', 'Attendance summary retrieved', 200, summary)