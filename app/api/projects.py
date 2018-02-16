from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from flask_login import login_required
from app.model import Project
from app import db
import re
from utils import json_error as je

project_fields = {
    'key': fields.String,
    'name': fields.String
}

class ProjectListResource(Resource):
    @login_required
    def get(self):
        return [marshal(proj) for proj in Project.query.all()]

    @login_required
    @marshal_with(project_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('key', required=True, help='Project key is missing')
        parser.add_argument('name', required=True, help='Project name is missing')
        args = parser.parse_args()

        e = re.compile('[a-zA-Z]{3,16}')
        if not e.fullmatch(args['key']):
            return {'status': 400, 'message': 'Key must only contain a-z'}, 400

        p = Project(args['key'].upper(), args['name'])
        return p, 201

class ProjectResource(Resource):
    @login_required
    def get(self, id):
        for item in Project.query.all():
            if item["id"] == id:
                return item
        abort(404)
