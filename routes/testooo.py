from flask_restful import Resource
from flask import jsonify, make_response, request

class test0(Resource):
    def get(self):
        return jsonify({"message": "hello world"})

    def post(self):
        data = request.get_json()
        message = "post working"
        return make_response(jsonify({"data": data, "message": message}), 201)

    def put(self):
        data = request.get_json()
        message = "put working"
        if data['demo'] == "demo":
            return make_response(jsonify({"data": data, "message": message}), 200)
        return make_response(jsonify({"data": data, "message": "data incorrect"}), 399)

    def delete(self):
        return make_response(jsonify({"message": "deleted"}), 204)