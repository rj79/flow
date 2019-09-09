from app.common import IssueType, issue_type_name
from app.model import Issue, Project
from database import db
from flask_login import login_required
from flask_restful import Resource, fields, marshal, marshal_with, request, reqparse
from utils import json_error as je

issue_created_fields = {
    'id': fields.Integer,
    'issue_type_id': fields.Integer,
    'title': fields.String,
    'description': fields.String
}

class IssueListResource(Resource):
    @login_required
    def get(self):
        return [marshal(i, issue_created_fields) for i in Issue.query.all()]

    @login_required
    @marshal_with(issue_created_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', required=True, type=int, help='Missing project_id')
        parser.add_argument('issue_type_id', required=True, type=int, help='Missing issue_type_id')
        parser.add_argument('title', required=True, help='Missing title')
        parser.add_argument('description', required=True, help='Missing description')
        args = parser.parse_args()
        p = Project.query.filter_by(id=args['project_id']).first()
        if p is None:
            p = Project.query.filter_by(key='DEFAULT').first()
            if p is None:
                p = Project('DEFAULT', 'Default project')
                db.session.add(p)
                db.session.commit()
        i = Issue(p, args['issue_type_id'], args['title'])
        i.description = args['description']
        db.session.add(i)
        db.session.commit()
        return i, 201


class IssueResource(Resource):
    @login_required
    @marshal_with(issue_created_fields)
    def get(self, id):
        i = Issue.query.get(id)
        if not i:
            abort(404, je('No issue with id {}'.format(id)))
        return issue


class IssueTypeListResource(Resource):
    @login_required
    def get(self):
        result = []
        for type_id in IssueType:
            result.append({'id': type_id, 'name': issue_type_name[type_id]})
        return result
