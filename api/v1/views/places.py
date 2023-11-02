#!/usr/bin/python3
"""View functions for `Place` objects"""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask imort Flask, jsonify, make_response, request

@app_views.route("/cities/<city_id>/places",
        mehtods=["GET"], strict_slashes=False)
def get_places(city_id):
    """Retieves all `Place` objects in a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = city.places
    list_places = [place.to_dict() for place in places]
    return jsonify(list_places)


@app_views.route("/places/<place_id>",
        methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a `Place` object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
        methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a `Place` object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
        mehtods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Creates a new `Place` object"""
    request_obj = request.get_json()
    
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request_obj is None:
        abort(400, "Not a JSON")
    if "user_id" not in request_obj:
        abort(400, "Missing user_id")
    
    user = storage.get("User", request_obj[user_id])
    if user is None:
        abort(404)

    if "name" not in request_obj:
        abort(400, "Missing name")

    request_obj["city_id"] = city_id
    new_place = Place(**request_obj)
    new_place.save()

    return make_response(jsonify(new_place), 201)

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a `Place` object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    request_obj = request.get_json()
    if request_obj is None:
        abort(400, "Not a JSON")

    for k,v in request_obj.items():
        if k not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, k, v)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
