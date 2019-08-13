import re
from .extension import parser
from marshmallow import fields, validate as validate_
from flask import jsonify


def parse_req(arg_map):
    return parser.parse(arg_map)


class FieldString(fields.String):
    DEFAULT_MAX_LENGTH = 1024  # 1 kB

    def __init__(self, validate=None, **metadata):
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldString, self).__init__(validate=validate, **metadata)


class FieldNumber(fields.Number):
    DEFAULT_MAX_LENGTH = 30  # 1 kB

    def __init__(self, validate=None, **metadata):
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldNumber, self).__init__(validate=validate, **metadata)


def send_result(data=None, message="OK", code=200, status=True):
    res = {
        "jsonrpc": "2.0",
        "status": status,
        "code": code,
        "message": message,
        "data": data,
    }

    return jsonify(res), 200


def check_password(password):
    if re.search(r"\s", password):
        return False
    if len(password) < 6:
        return False
    if re.search("[0-9]", password) is None:
        return False
    if re.search("[a-zA-Z]", password) is None:
        return False
    if re.search("[A-Z]", password) is None:
        return False
    return True