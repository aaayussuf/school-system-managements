from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..services.timetable_service import (
    get_timetable_entries,
    get_timetable_by_id,
    create_timetable_entry,
    update_timetable_entry,
    delete_timetable_entry
)
from ..utils.response_utils import make_response
from ..utils.auth_utils import roles_required

timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/', methods=['GET'])
@jwt_required()
def list_timetable():
    class_grade = request.args.get('class')
    teacher_id = request.args.get('teacher_id')
    day = request.args.get('day')
    term = request.args.get('term')
    
    timetable = get_timetable_entries(class_grade, teacher_id, day, term)
    return make_response('success', 'Timetable retrieved', 200, [t.to_dict() for t in timetable])

@timetable_bp.route('/<int:timetable_id>', methods=['GET'])
@jwt_required()
def get_timetable(timetable_id):
    entry = get_timetable_by_id(timetable_id)
    if not entry:
        return make_response('error', 'Timetable entry not found', 404)
    return make_response('success', 'Timetable entry retrieved', 200, entry.to_dict())

@timetable_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin')
def add_timetable():
    data = request.get_json()
    entry = create_timetable_entry(data)
    if not entry:
        return make_response('error', 'Failed to create timetable entry', 400)
    return make_response('success', 'Timetable entry created', 201, entry.to_dict())

@timetable_bp.route('/<int:timetable_id>', methods=['PUT'])
@jwt_required()
@roles_required('admin')
def modify_timetable(timetable_id):
    data = request.get_json()
    entry = update_timetable_entry(timetable_id, data)
    if not entry:
        return make_response('error', 'Timetable entry not found', 404)
    return make_response('success', 'Timetable entry updated', 200, entry.to_dict())

@timetable_bp.route('/<int:timetable_id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def remove_timetable(timetable_id):
    success = delete_timetable_entry(timetable_id)
    if not success:
        return make_response('error', 'Timetable entry not found', 404)
    return make_response('success', 'Timetable entry deleted', 200)