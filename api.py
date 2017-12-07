from flask_restful import Resource, Api

class IssueList(Resource):
    def post(self):
        

class Issue(Resource):
    def get(self):
        return {"title": "Title"}

def init_api(app):
    api = Api(app)
    api.add_resource(Issue, '/api/v1/issue/<string:key>')
