import hashlib
import random
import string

from models import session, Accounts
from services import elasticsearch_service


def signup(signup_request):
    same_name_count = session.query(Accounts).filter_by(name=signup_request['name']).count()
    same_email_count = session.query(Accounts).filter_by(email=signup_request['email']).count()

    if same_email_count > 0 or same_name_count > 0:
        return 'CREDENTIALS_ALREADY_EXIST'

    index = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(40))
    elasticsearch_service.create_index(index)

    new_account = Accounts(
        name=signup_request['name'],
        email=signup_request['email'],
        password=hashlib.sha256(signup_request['password'].encode('utf=8')).hexdigest(),
        index=index
    )

    session.add(new_account)
    session.commit()
    return 'ACCOUNT_CREATED'

