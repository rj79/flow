from flask import render_template
from app.admin import bp
from app.admin.forms import CreateProjectForm, CreateReleaseForm
from app.model import Project

@bp.route('/projects')
def projects():
    form = CreateProjectForm()
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects, project_form=form)

@bp.route('/project/<string:key>')
def project(key):
    p = Project.query.filter_by(key=key).first()
    form = CreateReleaseForm(project_id=p.id)
    form.project_id.choices = [(p.id, "{} - {}".format(p.key, p.name)) for p in Project.query.all()]
    return render_template('admin/project.html', project=p, release_form=form)
