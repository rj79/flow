from flask import make_response, render_template
from app.main import bp
from flask_login import current_user, login_required

@bp.route('/')
@login_required
def index():
    print('INDEX')
    return make_response("Hello")
    return render_template('index.html')
