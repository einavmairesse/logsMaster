import json
from elasticsearch import Elasticsearch
from models import session, Accounts
from services import authentication_service
from Config import ES_HOSTS

es = Elasticsearch(hosts=ES_HOSTS)


def create_index(index: str):
    es.indices.create(index)


def write(index: str, data: dict):
    result = es.index(index=index, body=json.dumps(data))
    if result['result'] != 'created':
        raise RuntimeError(f'Failed writing the doc {data} to es')


def search(query: dict, index: str):
    result = es.search(index=index, body=query)
    return result['hits']


def get_index_by_token(token: str):
    account_id = authentication_service.get_account_id_from_token(token)
    account = session.query(Accounts).filter_by(id=account_id).all()
    if len(account) == 1:
        return account[0].index
    else:
        return None
