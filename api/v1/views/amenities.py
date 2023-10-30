#!/usr/bin/python3
"""Module that handles all default RESTFUL API actions of Amenties"""
from models import storage
from flask import request, jsonify, abort, make_response
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """Endpoint tha handles amenties object or get req to an obj by ID"""
    amenities = storage.all('Amenity').values()
    if amenity_id is None:
        amenities_list = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities_list)
    else:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        else:
            abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Endpoint that handles delete of an obj by ID"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Endpoint that creates a new obj and adds to storage"""
    from models.amenity import Amenity
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    elif "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Endpoint to update an obj based on its ID"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        abort(404)
