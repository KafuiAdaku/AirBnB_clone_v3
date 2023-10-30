#!/usr/bin/python3
"""Module for Place Object and Amenitys object that handles all
default """
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Endpoint to get amenities based on place ID"""
    place = storage.get('Place', place_id)
    if place:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities = place.amenities
        else:
            ids = place.amenity_ids
            amenities = [storage.get('Place', id1) for id1 in ids]
        list_amenities = [amenity.to_dict() for amenity in amenities]
        return make_response(jsonify(list_amenities))
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """Endpoint to delete amenity based on place id and amenity id"""
    place = storage.get('Place', place_id)
    if place:
        amenity = storage.get('Amenity', amenity_id)
        if amenity and amenity in place.amenities:
            if storage_type == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity.id)
            place.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """Endpoint that links amenity to place obj"""
    place = storage.get('Place', place_id)
    if place:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            if amenity in place.amenities:
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                if storage_type == 'db':
                    place.amenities.append(amenity)
                else:
                    place.amenity_ids.append(amenity.id)
                place.save()
                return make_response(jsonify(amenity.to_dict()), 201)
        else:
            abort(404)
    else:
        abort(404)
