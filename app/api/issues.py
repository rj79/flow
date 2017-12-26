from flask_restful import Resource, fields, marshal_with, request, reqparse
from app import db
from app.model import Issue, Project
from app.common import IssueType, issue_type_name


issue_created_fields = {
    'id': fields.Integer,
    'issue_type': fields.Integer,
    'title': fields.String,
    'description': fields.String
}

class IssueListResource(Resource):
    def get(self):
        return issue_list

    @marshal_with(issue_created_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('issue_type', type=int, location='form', help='Missing type')
        parser.add_argument('title', location='form', help='Missing title')
        parser.add_argument('description', location='form')
        args = parser.parse_args()
        p = Project.query.filter_by(id=1).first()
        if p is None:
            p = Project('DEFAULT')
            db.session.add(p)
            db.session.commit()
        i = Issue(p, args['issue_type'], args['title'])
        i.description = args['description']
        db.session.add(i)
        db.session.commit()
        return i, 201


class IssueResource(Resource):
    def get(self, id):
        for issue in issue_list:
            print(issue)
            if issue["id"] == id:
                return issue
        abort(404)


class IssueTypeListResource(Resource):
    def get(self):
        result = []
        for type_id in IssueType:
            result.append({'id': type_id, 'name': issue_type_name[type_id]})
        return result
