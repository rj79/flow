from flask import render_template
from app.admin import bp
from app.admin.forms import CreateReleaseForm

@bp.route('/project')
def project():
    release_form = CreateReleaseForm()
    return render_template('admin/project.html', release_form=release_form)
