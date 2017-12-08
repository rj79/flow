from flask_restful import Resource

item_list = [{"id": 1, "name": "One Man Show"},
{"id": 2, "name": "The Squad"}]

class TeamList(Resource):
    def get(self):
        return item_list

class Team(Resource):
    def get(self, id):
        for item in item_list:
            if item["id"] == id:
                return item
        abort(404)
