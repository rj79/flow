from flask import Blueprint
from flask_restful import Api
from app.api import issues
bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(issues.IssueList, '/issues')
