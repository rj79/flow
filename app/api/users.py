from flask_restful import Resource

class User(Resource):
    def post(self, id):
        abort(404)


class Verification(Resource):
    def get(self, verification_code):
        pass
