from flask import render_template
from app.main import bp

@bp.route('/')
def board():
    return render_template('board.html')
