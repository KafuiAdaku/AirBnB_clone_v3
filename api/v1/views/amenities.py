#!/usr/bin/python3
"""View functions for `Amenity` objects"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves all amenity objects"""
    if not amenity_id:
        amenities = storage.all("Amenity")
        list_amnty =[amenity.to_dict() for amenity in amenities]
        return jsonify(list_amnty)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def add_amenity():
    """Adds a new `Amenity` object"""
    request_obj = request.get_json()
    if reqest_obj is None:
        abort(400, "Not a JSON")
    if "name" not in request_obj:
        abort(400, "Missing name")

    new_amenity = Amenity(**request_obj)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                methods=["PUT"], strict_slashes=False)
def update_amenity():
    """updates an `Amenity` object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    request_obj = request.get_json()
    if request_obj is None:
        abort(400, "Not a JSON")
    if "name" not in request_obj:
        abort(400, "missing name")

    for k,v in request_obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
