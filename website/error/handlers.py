from flask import Blueprint, render_template
from flask_login import current_user

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', user=current_user), 404

@errors.app_errorhandler(403)
def forbidden_request(error):
    return render_template('errors/403.html', user=current_user), 403

@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', user=current_user), 500