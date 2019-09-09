from app.model import Project, Release
from database import db
from datetime import date, datetime
from flask import abort
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_login import login_required
from utils import json_error as je

class DateField(fields.Raw):
    def format(self, value):
        return value.strftime('%Y%m%d')

release_fields = {
    'name': fields.String,
    'release_date': DateField,
    'project_id': fields.Integer
}

class ReleaseListResource(Resource):
    @login_required
    def get(self):
        rl = [ marshal(r, release_fields) for r in Release.query.all() ]
        return rl

    @login_required
    @marshal_with(release_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Release name is missing')
        parser.add_argument('release_date', required=True, help='Release date is missing')
        parser.add_argument('project_id', required=True, type=int, help='Project id is missing')
        args = parser.parse_args()

        try:
            date = datetime.strptime(args['release_date'], '%Y%m%d').date()
        except ValueError:
            abort(400, je('Invalid date'))

        p = Project.query.get(args['project_id'])
        if not p:
            abort(400, je('Invalid project'))

        r = p.create_release(args['name'], date)
        db.session.add(r)
        db.session.commit()
        return r, 201

class ReleaseResource(Resource):
    @login_required
    def get(self, id):
        r = Release.query.get(id)
        if not r:
            abort(404, 'No release with id {} found')
        return r

    @login_required
    def put(self, id):
        return '', 400
