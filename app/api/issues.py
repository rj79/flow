from flask_restful import Resource

class IssueList(Resource):
    def get(self):
        stuff = [{"id": 1, "title": "Issue 1"}, {"id": 2, "title": "Issue 2"}]
        return stuff
