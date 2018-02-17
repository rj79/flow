from flask import make_response, render_template
from flask_login import current_user, login_required
from app.common import IssueType, issue_type_name
from app.main import bp
from app.main.forms import CreateIssueForm
from app.model import Issue, Project

@bp.route('/')
@login_required
def index():
    issues = Issue.query.all()
    form = CreateIssueForm()
    form.project_id.choices = [(p.id, "{} - {}".format(p.key, p.name)) for p in Project.query.all()]
    form.issue_type_id.choices = [(int(t), issue_type_name[int(t)]) for t in IssueType]
    return render_template('index.html', issues=issues, form=form)
