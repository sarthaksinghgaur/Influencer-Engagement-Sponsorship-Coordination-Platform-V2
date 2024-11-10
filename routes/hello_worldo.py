from flask_restful import Resource
from flask import jsonify, make_response, request
from models import *
from flask_login import current_user

class hello_worldo(Resource):
    def get(self):
        from models import db
        for obj in db.session.identity_map.values():
            print(obj)
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

    def patch(self):
        response_data = {}
        for obj in db.session.identity_map.values():
            if isinstance(obj, Role):
                obj_data = {"id": obj.id, "name": obj.name}
            elif isinstance(obj, User):
                obj_data = {"id": obj.id, "email": obj.email, "username": obj.username}
            response_data[f"{obj.__class__.__name__}_{obj.id}"] = obj_data
        return make_response(jsonify(response_data), 200)
    
    def options(self):
        user = current_user
        print(user.id)
        sponsor = Sponsor.query.filter(Sponsor.id == user.id).all()
        print(sponsor)
        return jsonify({"message": "options working"})
    
