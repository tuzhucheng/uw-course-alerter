from flask import Response
from flask import make_response, request


def make_error_response(res_body, code=400, mimetype='text/plain'):
    res = Response(res_body, code, mimetype=mimetype)
    return make_response(res)


def validate_fields_exist(required_fields):
    missed_fields = []
    for required_field in required_fields:
        if not required_field in request.form:
            missed_fields.append(required_field)

    if len(missed_fields):
        res_body = 'The following fields are missing:\n'
        for m in missed_fields:
            res_body += m + '\n'
        return False, make_error_response(res_body)

    return True, None

