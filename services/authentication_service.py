import datetime
import hashlib
import random
import string

from models import session, AccountToken, Accounts


def login(login_request):
    hashed_password = hashlib.sha256(login_request['password'].encode('utf-8')).hexdigest()
    matching_accounts = session.query(Accounts).filter_by(email=login_request['email']).filter_by(password=hashed_password).all()

    if len(matching_accounts) != 1:
        return 'FAILED_LOGIN'

    account = matching_accounts[0]
    existing_tokens = session.query(AccountToken).filter_by(account_id=account.id).all()
    if len(existing_tokens) == 1 and existing_tokens[0].update_date + datetime.timedelta(days=1) < datetime.datetime.now() or len(existing_tokens) == 0:
        account_token = AccountToken(
            account_id=account.id,
            token=''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30)),
            update_date=datetime.datetime.now()
        )
        session.add(account_token)
        session.commit()

    return session.query(AccountToken).filter_by(account_id=account.id).one().token


def is_valid_token(token: str):
    account_token_relation = session.query(AccountToken).filter_by(token=token).all()
    if len(account_token_relation) != 1:
        return False

    return True


def get_account_id_from_token(token: str):
    account_token_relation = session.query(AccountToken).filter_by(token=token).all()
    if len(account_token_relation) == 1:
        return account_token_relation[0].account_id

    return None
