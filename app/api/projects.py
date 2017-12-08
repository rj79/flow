from flask_restful import Resource

item_list = [{"id": 1, "name": "Flow", "key": "FLOW"},
{"id": 2, "name": "ProjectTwo", "key": "PTWO"}]

class ProjectList(Resource):
    def get(self):
        return item_list

class Project(Resource):
    def get(self, id):
        for item in item_list:
            if item["id"] == id:
                return item
        abort(404)
