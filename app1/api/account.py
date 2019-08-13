from flask import Blueprint
from app1.extension import parser, jwt, client
from datetime import timedelta
from flask_restful import reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from app1.utils import FieldString, parse_req, send_result, check_password
from bson.objectid import ObjectId
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, get_jwt_identity,
    create_refresh_token, get_raw_jwt, get_jti,
    get_jwt_claims
    )


api = Blueprint('account', __name__)

ACCESS_EXPIRES = timedelta(days=1)
REFRESH_EXPIRES = timedelta(days=1)

@api.route('/register', methods=['POST'])
def register():
    params = {
        'username': FieldString(),
        'password': FieldString(),
        'role': FieldString(),
        'status': FieldString()
    }

    json_data = parse_req(params)
    username = json_data.get('username').strip().lower()
    password = json_data.get('password')
    role = json_data.get('role')
    status = json_data.get('status')

    user = client.db.user.find_one({'username': username})
    if user:
        return 'That username already existed'

    tmp = {"username": username, "password": generate_password_hash(password), "role": role, "status": status,
           "deleted": False, "_id": str(ObjectId())}

    client.db.user.insert_one(tmp)
    return send_result(data={
        'username': username,
        'password': password,
        'role': role,
        'status': status},
        message='register_successfully')


@api.route('/login', methods=['POST'])
def login():
    params = {
        'username': FieldString(),
        'password': FieldString()
    }
    json_data = parse_req(params)
    username = json_data.get('username').strip().lower()
    password = json_data.get('password')

    user = client.db.user.find_one({'username': username, 'deleted': False})
    if user:
        activate = user['status']
        if activate == 'activated' and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=user['_id'], expires_delta=ACCESS_EXPIRES)
            refresh_token = create_refresh_token(identity=user['_id'], expires_delta=REFRESH_EXPIRES)
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            user_token = dict(
                _id=str(ObjectId()),
                user_id=user['_id'],
                access_jti=access_jti,
                refresh_jti=refresh_jti
            )
            client.db.token.insert_one(user_token)
            return send_result(data={'access_token': access_token,
                                     'refresh_token': refresh_token,
                                     'role': user['role']
                                     },
                               message='login_successfully')
    else:
        return 'Login failed'


@api.route('/update_password', methods=['PUT'])
@jwt_required
def update_password():
    claims = get_jwt_claims()
    if not claims["is_admin"]:
        return 'You need admin right'
    params = {
        'user_id': FieldString(),
        'password': FieldString()
    }

    json_data = parse_req(params)
    user_id = json_data.get('user_id')
    password = json_data.get('password')

    user = client.db.user.find_one({"_id": user_id})
    if user is None:
        return'That id was not existed'

    query = {"_id": user_id}
    new_values = {"$set": {"password": generate_password_hash(password)}}
    client.db.user.update_one(query, new_values)

    return send_result(data={
        'username':  user['username'],
        'new password': generate_password_hash(password)
        },
        message='update_password_successfully')
