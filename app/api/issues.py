from flask_restful import Resource
import common

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

class IssueTypeList(Resource):
    def get(self):
        result = []
        for type_id in common.IssueType:
            result.append({'id': type_id, 'name': common.issue_type_name[type_id]})
        return result
