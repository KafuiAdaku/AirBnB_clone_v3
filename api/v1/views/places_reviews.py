#!/usr/bin/python3
"""View functions for `Review` object"""
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import abort, Flask, jsonify, make_response, request

@app_views.route("/places/<place_id>/reviews",
                methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves all `Review` objects linked to a `Place` object"""
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    reviews = place.reviews
    rev_list = [review.to_dict() for review in reviews]
    return jsonify(rev_list)

@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a `Review` object linked to a `Place` object"""
    request_obj = request.get_json()
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    if request_obj is None:
        return abort(400, "Not a JSON")
    if "user_id" not in request_obj:
        return abort(400, "Missing user_id")
    user = storage.get("User", request_obj["user_id"])
    if  user is None:
        return abort(404)
    if "text" not in request_obj:
        return abort(400, "Missing text")

    request_obj["place_id"] = place_id
    review = Review(**request_obj)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)

@app_views.route("/reviews/<review_id>",
                methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a `Review` object"""
    review = storage.get("Review", review_id)
    if review is None:
        return abort(404)

    request_obj = request.get_json()
    if request_obj is None:
        return abort(404, "Not a JSON")

    for k,v in request_obj.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, k, v)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
