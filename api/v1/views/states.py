#!/usr/bin/python3
"""module for the RESTFUL api view for State"""
from models.state import State
from models import storage
from flask import Flask, request, jsonify, abort, make_response
from api.v1.views import app_views


@app_views.route('/states/', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def show_states(state_id=None):
    """End point to access object of State"""
    states = storage.all(State).values()
    if state_id is None:
        states_list = [state.to_dict() for state in states]
        return jsonify(states_list)
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """End point to delete obj from state objs"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Endpoint for adding new state obj to the database"""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    elif "name" not in body:
        abort(400, "Missing name")
    else:
        state = State(**body)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Endpoint for updating a state obj"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        body = request.get_json()
        if body is None:
            abort(400, "Not a JSON")

        for key, value in body.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
