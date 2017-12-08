from flask_restful import Resource

issue_list = [{"id": 1, "title": "Issue 1"}, {"id": 2, "title": "Issue 2"}]

class IssueList(Resource):
    def get(self):
        return issue_list

class Issue(Resource):
    def get(self, id):
        for issue in issue_list:
            print(issue)
            if issue["id"] == id:
                return issue
        abort(404)
