from flask import Blueprint
from flask_restful import Api
from app.api import issues, projects, releases, teams

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(issues.IssueListResource, '/issues', endpoint='issues')
api.add_resource(issues.IssueResource, '/issues/<int:id>')

api.add_resource(issues.IssueTypeListResource, '/issue_types')

api.add_resource(projects.ProjectListResource, '/projects', endpoint='projects')
api.add_resource(projects.ProjectResource, '/projects/<int:id>')

api.add_resource(releases.ReleaseListResource, '/releases', endpoint='releases')
api.add_resource(releases.ReleaseResource, '/releases/<int:id>')

api.add_resource(teams.TeamListResource, '/teams')
api.add_resource(teams.TeamResource, '/teams/<int:id>')
