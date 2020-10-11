from flask import Blueprint

general_bp = Blueprint('general', __name__)


@general_bp.route('/health')
def health():
    return 'App is running'
