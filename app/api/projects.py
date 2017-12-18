from flask_restful import Resource, fields, marshal, marshal_with
from app import db

project_fields = {
    'key': fields.String,
    'name': fields.String
}

class ProjectList(Resource):
    def get(self):
        return [marshal(proj) for proj in model.Project.query.all()], 200

    @marshal_with(project_fields)
    def post(self, key):
        p = Project(key)
        db.session.add(p)
        try:
            db.commmit()
        except:
            return 404
        return p, 201


class Project(Resource):
    def get(self, id):
        for item in Project.query.all():
            if item["id"] == id:
                return item
        abort(404)
