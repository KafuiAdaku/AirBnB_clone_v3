#!/usr/bin/python3
"""Module that handles the cities objs RESTFUL api"""
from api.v1.views import app_views
from flask import make_response, jsonify, request, abort
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """endpoint for accessing a state object"""
    state = storage.get('State', state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return make_response(jsonify(cities))
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Endpoint for adding an obj to cities"""
    state = storage.get('State', state_id)
    if state:
        from models.city import City
        data = request.get_json()
        if not data:
            return abort(400, 'Not a JSON')
        elif 'name' not in data:
            return abort(400, 'Missing name')
        city = City(name=data['name'])
        city.state_id = state_id
        city.save()
        return make_response(jsonify(city.to_dict()), 201)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Endpoint to get a city by its ID"""
    city = storage.get('City', city_id)
    if city:
        return make_response(jsonify(city.to_dict()))
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Endpoint to delete a city object by ID"""
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Endpoint to update a city obj by ID"""
    city = storage.get('City', city_id)
    if city:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, val in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
    else:
        abort(404)
