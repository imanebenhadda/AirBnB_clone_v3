#!/usr/bin/python3
"""view for Review objects that handles all default RESTFul API actions"""
from flask import jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["GET"])
@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def reviews(place_id=None, review_id=None):
    """Retrieves the list of all review objects of a reviews
    Retrieves a reviews object.
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            result = []
            allreviews = place.reviews
            for review in allreviews:
                result.append(review.to_dict())
            return jsonify(result), 200
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """return a JSON: delete a review object that match review_id
    or Not found if the id not match any exist review"""
    review = storage.get(Review, review_id)
    if review is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """
    If the place_id is not linked to any City object, raise a 404 error
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn't contain the key text,
    raise a 400 error with the message Missing text
    If the dictionary doesn't contain the key user_id,
    raise a 400 error with the message Missing user_id
    Returns the new review with the status code 201
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if not storage.get(Place, place_id):
            return make_response(jsonify({"error": "Not found"}), 404)

        if "user_id" not in json_data:
            return make_response("Missing user_id", 400)

        if not storage.get(User, json_data["user_id"]):
            return make_response(jsonify({"error": "Not found"}), 404)

        if "text" not in json_data:
            return make_response("Missing text", 400)

        json_data["place_id"] = place_id
        instance = Review(**json_data)
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)
    return make_response("Not a JSON", 400)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def Update_Review(review_id):
    """update Review"""
    review = storage.get(Review, review_id)
    if review is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    review.text = data.get("text", review.text)
    review.save()
    return jsonify(review.to_dict()), 200
