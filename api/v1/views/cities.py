#!/usr/bin/python3
"""State objects that handles all default RESTFul API"""

from flask import jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=["GET"])
@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def cities(state_id=None, city_id=None):
    """Retrieves the list of all City objects of a State"""
    if state_id:
        state = storage.get(State, state_id)
        if state:
            result = []
            cities = state.cities
            for city in cities:
                result.append(city.to_dict())
            return jsonify(result), 200
    if city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """return a JSON: delete a state object that match city_id
    or Not found if id not exist"""
    city = storage.get(City, city_id)
    if city is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=["POST"])
def Create_city(state_id):
    """
    If the state_id is not linked to any State object
        raise a 404 error
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON
    If the dictionary doesn't contain the key name,
        raise a 400 error with the message Missing name
    Returns: the new State with the status code 201
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if not storage.get(State, state_id):
            return make_response(jsonify({"error": "Not found"}), 404)
        if "name" in json_data:
            json_data["state_id"] = state_id
            instance = City(**json_data)
            instance.save()
            return make_response(jsonify(instance.to_dict()), 201)
        else:
            return make_response("Missing name", 400)
    else:
        return make_response("Not a JSON", 400)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def Update_city(city_id):
    """update city"""
    obj = storage.get(City, city_id)
    if obj is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
