from flask_restful import Resource

item_list = [{"id": 1, "name": "R1", "date": "2017-12-08T21:42:00Z"},
{"id": 2, "name": "R2", "date": "2018-01-01T10:01:00Z"}]

class ReleaseList(Resource):
    def get(self):
        return item_list

class Release(Resource):
    def get(self, id):
        for item in item_list:
            if item["id"] == id:
                return item
        abort(404)
