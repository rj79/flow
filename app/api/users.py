from flask_restful import Resource
from utils import json_error as je

class UserResource(Resource):
    def post(self, id):
        abort(404)


class Verification(Resource):
    def get(self, verification_code):
        pass
