from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from services.fee_service import (
    get_all_fees,
    get_fee_by_id,
    create_fee,
    update_fee,
    delete_fee,
    get_fee_summary
)
from utils.response_utils import make_response
from utils.auth_utils import roles_required

fees_bp = Blueprint('fees', __name__)

@fees_bp.route('/', methods=['GET'])
@jwt_required()
def list_fees():
    student_id = request.args.get('student_id')
    class_grade = request.args.get('class')
    status = request.args.get('status')
    term = request.args.get('term')
    
    fees = get_all_fees(student_id, class_grade, status, term)
    return make_response('success', 'Fees retrieved', 200, [f.to_dict() for f in fees])

@fees_bp.route('/<int:fee_id>', methods=['GET'])
@jwt_required()
def get_fee(fee_id):
    fee = get_fee_by_id(fee_id)
    if not fee:
        return make_response('error', 'Fee record not found', 404)
    return make_response('success', 'Fee retrieved', 200, fee.to_dict())

@fees_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin')
def add_fee():
    data = request.get_json()
    fee = create_fee(data)
    if not fee:
        return make_response('error', 'Failed to create fee record', 400)
    return make_response('success', 'Fee record created', 201, fee.to_dict())

@fees_bp.route('/<int:fee_id>', methods=['PUT'])
@jwt_required()
@roles_required('admin')
def modify_fee(fee_id):
    data = request.get_json()
    fee = update_fee(fee_id, data)
    if not fee:
        return make_response('error', 'Fee record not found', 404)
    return make_response('success', 'Fee record updated', 200, fee.to_dict())

@fees_bp.route('/<int:fee_id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def remove_fee(fee_id):
    success = delete_fee(fee_id)
    if not success:
        return make_response('error', 'Fee record not found', 404)
    return make_response('success', 'Fee record deleted', 200)

@fees_bp.route('/summary', methods=['GET'])
@jwt_required()
@roles_required('admin')
def fee_summary():
    summary = get_fee_summary()
    return make_response('success', 'Fee summary retrieved', 200, summary)