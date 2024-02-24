#!/usr/bin/python3
"""Create a new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""
from flask import jsonify, make_response

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False,
                 methods=["GET"])
def Amenities(place_id):
    """return a JSON: list of all Amenities objects or one Amenities,
    Or not found if id not exsit"""
    place = storage.get(Place, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    Amenities = []
    if storage_t == "db":
        amenities = place.amenities
        for amenity in amenities:
            Amenities.append(amenity.to_dict())
    else:
        Amenities = place.amenity_ids
    return jsonify(Amenities), 200


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    strict_slashes=False,
    methods=["DELETE"],
)
def delete_Amenity(place_id, amenity_id):
    """return a JSON: delete a Amenity object that match <amenity_id>
    or Not found if id not exist"""
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    if storage_t == "db":
        amenities = place.amenities
        if amenity not in amenities:
            return make_response(jsonify({"error": "Not found"}), 404)
    else:
        if amenity_id not in place.amenity_ids:
            return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["POST"])
def link_Amenity_place(place_id, amenity_id):
    """
    No HTTP body needed
    If the place_id is not linked to any Place object
        raise a 404 error
    If the amenity_id is not linked to any Amenity object
        raise a 404 error
    If the Amenity is already linked to the Place
        return the Amenity with the status code 200
    Returns the Amenity with the status code 201
    """
    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    if storage_t == "db":
        amenities = place.amenities
        if amenity in amenities:
            return amenity.to_dict(), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return amenity.to_dict(), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return amenity.to_dict(), 201
