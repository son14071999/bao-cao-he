from flask import Blueprint
from app1.extension import parser, jwt, client
from app1.utils import FieldString, parse_req, send_result, check_password, FieldNumber
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_claims


api = Blueprint('L_O_A', __name__)


@api.route('/create_form', methods=['POST'])
@jwt_required
def create_form():
    params = {
        'email': FieldString(),
        'name': FieldString(),
        'role': FieldString(),
        'reason': FieldString(),
        'note': FieldString()
    }

    json_data = parse_req(params)
    email = json_data.get('email')
    name = json_data.get('name')
    role = json_data.get('role')
    reason = json_data.get('reason')
    approve_code = 0
    admin_approve = ''
    note = json_data.get('note')

    form = {"_id": str(ObjectId()), 'email': email, 'name': name, 'role': role,
            'reason': reason, 'approve_code': approve_code,
            'admin_approval': admin_approve, 'note': note}
    client.db.loa_form.insert_one(form)
    return send_result(data={
        'email': email,
        'name': name,
        'role': role,
        'reason': reason,
        'note': note,
        'approve_code': approve_code},
        message='LOA form created, waiting for admin to approve')


@api.route('/get_unapproved_form', methods=['POST'])
@jwt_required
def get_unapproved_form():
    claims = get_jwt_claims()
    if not claims["is_admin"]:
        return 'You cant access this'
    temp = client.db.loa_form.find({'approve_code': 0})
    # print(temp['email'])
    return send_result(
        data={"list_form": [form for form in temp]},
        message='list_forms'
    )


@api.route('/get_all_form', methods=['POST'])
@jwt_required
def get_all_form():
    claims = get_jwt_claims()
    if not claims["is_admin"]:
        return 'You cant access this'
    temp = client.db.loa_form.find()
    return send_result(
        data={"list_form": [form for form in temp]},
        message='list_forms'
    )


@api.route('/get_follow_people', methods=['POST'])
@jwt_required
def get_follow_people():
    params = {
        'user_name': FieldString()
    }
    json_data = parse_req(params)
    user_name = json_data.get('user_name')
    user = client.db.user.find_one({'username':user_name})
    name = user['username']
    temp = client.db.loa_form.find({'name': name})
    if temp != []:
        return send_result(
            data={"list_form": [form for form in temp]},
            message='list_forms'
        )
    else:
        return "not found"


@api.route('/admin_approve', methods=['POST'])
@jwt_required
def admin_approve():
    claims = get_jwt_claims()
    if not claims["is_admin"]:
        return 'You cant access this'

    params = {
        'code': FieldString(),
        'form_id': FieldString()
    }
    json_data = parse_req(params)
    code = json_data['code']
    form_id = json_data['form_id']

    client.db.loa_form.update_one({'_id': form_id}, {'$set': {'approve_code': code}})
    form = client.db.loa_form.find_one({'_id': form_id})
    if code == "1":
        return send_result(data={
            'email': form['email'],
            'name': form['name'],
            'role': form['name'],
            'reason': form['reason'],
            'note': form['note'],
            'approve_code': form['approve_code']},
            message='LOA form approved')
    else:
        return send_result(data={
            'email': form['email'],
            'name': form['name'],
            'role': form['name'],
            'reason': form['reason'],
            'note': form['note'],
            'approve_code': form['approve_code']},
            message='LOA form denied')
