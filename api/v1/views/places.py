#!/usr/bin/python3
"""import module"""
from flask import jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["GET"])
@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def places(city_id=None, place_id=None):
    """Retrieves the list of all Place objects of a City
    Retrieves a Place object.
    """
    if city_id:
        city = storage.get(City, city_id)
        if city:
            result = []
            allplaces = city.places
            for place in allplaces:
                result.append(place.to_dict())
            return jsonify(result), 200
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """return a JSON: delete a Place object that match place_id
    or Not found if the id not match any exist Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """
    If the city_id is not linked to any City object, raise a 404 error
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key user_id,
    raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object,
    raise a 404 error
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    Returns the new Place with the status code 201
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if not storage.get(City, city_id):
            return make_response(jsonify({"error": "Not found"}), 404)

        if "user_id" not in json_data:
            return make_response("Missing user_id", 400)

        user_id = json_data["user_id"]
        if not storage.get(User, user_id):
            return make_response(jsonify({"error": "Not found"}), 404)

        if "name" not in json_data:
            return make_response("Missing name", 400)

        json_data["city_id"] = city_id
        instance = Place(**json_data)
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)
    return make_response("Not a JSON", 400)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_placey(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    place.name = data.get("name", place.name)
    place.description = data.get("description",
                                 place.description)
    place.number_rooms = data.get("number_rooms",
                                  place.number_rooms)
    place.number_bathrooms = data.get("number_bathrooms",
                                      place.number_bathrooms)
    place.max_guest = data.get("max_guest", place.max_guest)
    place.price_by_night = data.get("price_by_night", place.price_by_night)
    place.latitude = data.get("latitude", place.latitude)
    place.longitude = data.get("longitude", place.longitude)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search",
                 strict_slashes=False,
                 methods=["POST"])
def places_search():
    """
    Search Places:
    That retrieves all Place objects depending of the JSON
    in the body of the request.
    The JSON can contain 3 optional keys:
    states: list of State ids
    cities: list of City ids
    amenities: list of Amenity ids
    """
    json_data = request.get_json(force=True, silent=True)
    # print(json_data)
    if json_data is None:
        return make_response("Not a JSON", 400)
    result = []
    if len(json_data) == 0 or \
            all(value == [] for value in json_data.values()):
        places = storage.all(Place).values()
        for place in places:
            result.append(place.to_dict())
        return jsonify(result)

    for state_id in json_data.get("states", []):
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                if city:
                    for place in city.places:
                        result.append(place)

    for city_id in json_data.get("cities", []):
        city = storage.get(City, city_id)
        if city:
            for place in city.places:
                if place not in result:
                    result.append(place)

    if len(result) == 0:
        result = list(storage.all(Place).values())
    for place in result.copy():
        for amenity_id in json_data.get("amenities", []):
            amenity = storage.get(Amenity, amenity_id)
            if amenity not in place.amenities:
                result.remove(place)
                break

    places = []
    for place in result:
        place_dict = place.to_dict()
        if 'amenities' in place_dict:
            del place_dict['amenities']
        places.append(place_dict)
    return jsonify(places), 200
