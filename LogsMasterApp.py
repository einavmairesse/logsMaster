from flask import Flask

from routes.log_shipping_route import send_logs_bp
from routes.account_management_route import account_management_bp
from routes.search_route import search_bp
from routes.general_route import general_bp

logsMasterApp = Flask(__name__)
logsMasterApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    logsMasterApp.register_blueprint(send_logs_bp)
    logsMasterApp.register_blueprint(account_management_bp)
    logsMasterApp.register_blueprint(search_bp)
    logsMasterApp.register_blueprint(general_bp)

    logsMasterApp.run(host='0.0.-0.0', port=5000)
