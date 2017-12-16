from flask import Blueprint
from flask_restful import Api
from app.api import issues, projects, releases, teams

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(issues.IssueListResource, '/issues')
api.add_resource(issues.IssueResource, '/issues/<int:id>')

api.add_resource(issues.IssueTypeListResource, '/issue_types')

api.add_resource(projects.ProjectList, '/projects')
api.add_resource(projects.Project, '/projects/<int:id>')

api.add_resource(releases.ReleaseList, '/releases')
api.add_resource(releases.Release, '/releases/<int:id>')

api.add_resource(teams.TeamList, '/teams')
api.add_resource(teams.Team, '/teams/<int:id>')
