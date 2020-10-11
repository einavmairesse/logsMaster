from flask import Blueprint, request

from error_codes import BAD_REQUEST, CREATED, UNAUTHORIZED, OK
from services import signup_service, authentication_service

account_management_bp = Blueprint('account_management', __name__)


@account_management_bp.route('/signup', methods=['POST'])
def signup():
    if 'name' not in request.json or 'email' not in request.json or 'password' not in request.json:
        return 'MISSING_SIGNUP_DATA', BAD_REQUEST

    signup_request = request.json
    result = signup_service.signup(signup_request)
    if result == 'ACCOUNT_CREATED':
        return 'ACCOUNT_CREATED', CREATED
    else:
        return 'CREDENTIALS_ALREADY_EXIST', BAD_REQUEST


@account_management_bp.route('/login', methods=['POST'])
def login():
    if 'email' not in request.json or 'password' not in request.json:
        return 'MISSING_LOGIN_DATA', BAD_REQUEST

    login_request = request.json
    login_result = authentication_service.login(login_request)

    if login_result == 'FAILED_LOGIN':
        return 'FAILED_LOGIN', UNAUTHORIZED
    else:
        return login_result, OK
