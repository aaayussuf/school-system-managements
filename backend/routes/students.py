from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from services.student_service import (
    get_all_students, 
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)
from utils.response_utils import make_response
from utils.auth_utils import roles_required

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    class_grade = request.args.get('class')
    students = get_all_students(class_grade)
    return make_response('success', 'Students retrieved', 200, [s.to_dict() for s in students])

@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return make_response('error', 'Student not found', 404)
    return make_response('success', 'Student retrieved', 200, student.to_dict())

@students_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin')
def add_student():
    data = request.get_json()
    student = create_student(data)
    if not student:
        return make_response('error', 'Failed to create student', 400)
    return make_response('success', 'Student created', 201, student.to_dict())

@students_bp.route('/<int:student_id>', methods=['PUT'])
@jwt_required()
@roles_required('admin')
def modify_student(student_id):
    data = request.get_json()
    student = update_student(student_id, data)
    if not student:
        return make_response('error', 'Student not found', 404)
    return make_response('success', 'Student updated', 200, student.to_dict())

@students_bp.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def remove_student(student_id):
    success = delete_student(student_id)
    if not success:
        return make_response('error', 'Student not found', 404)
    return make_response('success', 'Student deleted', 200)