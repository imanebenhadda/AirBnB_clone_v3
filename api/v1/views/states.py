#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import make_response, request, jsonify


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """return a JSON: list of all State objects or one State,
    Or not found if id not exsit"""
    if state_id is None:
        result = []
        states = storage.all(State).values()
        for state in states:
            result.append(state.to_dict())
        return jsonify(result)
    else:
        state = storage.get(State, state_id)
        if state is None:
            return make_response(jsonify({"error": "Not found"}), 404)
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_states(state_id):
    """return a JSON: delete a state object that match State_id
    or Not found if id not exist"""
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def Create_state():
    """
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON
    If the dictionary doesn't contain the key name,
        raise a 400 error with the message Missing name
    Returns: the new State with the status code 201
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if "name" in json_data:
            instance = State(**json_data)
            instance.save()
            return make_response(jsonify(instance.to_dict()), 201)
        else:
            return make_response("Missing name", 400)
    else:
        return make_response("Not a JSON", 400)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def Update_state(state_id):
    """
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON
    Returns: the new State with the status code 200
    """
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
