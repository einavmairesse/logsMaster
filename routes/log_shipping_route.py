from flask import Blueprint, request
from services import elasticsearch_service, authentication_service
from error_codes import BAD_REQUEST, UNAUTHORIZED, CREATED

send_logs_bp = Blueprint('logShipping', __name__)


@send_logs_bp.route('/send_logs', methods=['POST'])
def send_logs():
    if request.json is None:
        return 'NO_BODY', BAD_REQUEST
    elif 'token' not in request.json:
        return 'MISSING_TOKEN', UNAUTHORIZED
    elif 'logs' not in request.json:
        return 'NO_LOGS_SENT', BAD_REQUEST

    token = request.json['token']
    if not authentication_service.is_valid_token(token):
        return 'INVALID_TOKEN', UNAUTHORIZED

    index = elasticsearch_service.get_index_by_token(token)
    shipped_logs = request.json['logs']

    if len(shipped_logs) == 0:
        return 'EMPTY_LIST', BAD_REQUEST

    for log in shipped_logs:
        elasticsearch_service.write(index, log)

    return 'CREATED', CREATED
