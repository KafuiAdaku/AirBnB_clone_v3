#!/usr/bin python3
"""View functions for `City` object"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort, make_response, Flask, jsonify, request

@app_views.route("/states/<state_id>/cities",
                methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """Retrieves all cities in a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = state.cities
    if cities:
        list_cities = [city.to_dict() for city in cities]
        return jsonify(list_cities)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retieives a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort (404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """Creates a `Cityy` object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_obj = request.get_json()
    if request_obj is None:
        abort(404, "Not a JSON")
    if "name" not in request_obj:
        abort(404, "Missing name")

    new_city = City(**request_obj)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>",
        methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """updates a `City` object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_obj = request.get_json()
    if request_obj is None:
        abort(404, "Not a JSON")

    for k,v in request_obj.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
