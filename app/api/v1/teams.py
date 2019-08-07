from flask_restful import Resource, fields, marshal_with
from flask_login import login_required
from app.model import Team
from utils import json_error as je

team_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class TeamListResource(Resource):
    @login_required
    @marshal_with(team_fields)
    def get(self):
        return Team.query.all()

class TeamResource(Resource):
    @login_required
    def get(self, id):
        t = Team.query.get(int(id))
        if not t:
            abort(404, je('No team with id {}'.format(id)))
