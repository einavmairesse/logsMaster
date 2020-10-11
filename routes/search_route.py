import json

from flask import Blueprint, request

from error_codes import BAD_REQUEST, UNAUTHORIZED
from services import authentication_service, elasticsearch_service

search_bp = Blueprint('queries', __name__)


@search_bp.route('/search', methods=['POST'])
def search():
    if 'query' not in request.json:
        return 'NO_QUERY_PROVIDED', BAD_REQUEST

    if 'token' not in request.json:
        return 'MISSING_TOKEN', UNAUTHORIZED

    token = request.json['token']
    query = {'query': request.json['query']}

    if not authentication_service.is_valid_token(token):
        return 'INVALID_TOKEN', UNAUTHORIZED

    index = elasticsearch_service.get_index_by_token(token)
    result = elasticsearch_service.search(query, index)
    return json.dumps(result['hits'])

