from flask import Blueprint
from flask_restful import Api
from app.api import issues
from app.api import projects

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(projects.ProjectList, '/projects')
api.add_resource(projects.Project, '/projects/<int:id>')

api.add_resource(issues.IssueList, '/issues')
api.add_resource(issues.Issue, '/issues/<int:id>')
