#!/usr/bin/python3
"""Module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from flask import Flask, request, jsonify, abort, make_response
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """method that gets all reviews of a place by place ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        places_reviews = storage.all(Review).values()
        reviews = [review.to_dict() for review in places_reviews
                   if review.place_id == place_id]
        return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """Endpoint to get review by review ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Endpoint to delete a review based on its ID provided"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Endpoint to create a review in database"""
    body = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if body is None:
        abort(400, "Not a JSON")
    if "user_id" not in body:
        abort(400, "Missing user_id")

    user_id = body.get('user_id')

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    if "text" not in body:
        abort(400, "Missing text")

    review = Review(**body)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Endpoint to update a review based on its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    body = request.get_json()

    if body is None:
        abort(400, "Not a JSON")

    for key, value in body.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
