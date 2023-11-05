#!/usr/bin/python3
"""A module that defines a view functions for the `State` class"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, abort, request

@app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves all `State` objects"""
    if state_id is None:
        all_states = storage.all("State").values()
        list_obj = [state.to_dict() for state in all_states]
        return jsonify(list_obj)

    obj = storage.get("State", state_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    else:
        return abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                strict_slashes=False)
def del_state(state_id):
    """Deletes a state object by its state ID"""
    del_obj = storage.get("State", state_id)
    if del_obj is not None:
        storage.delete(del_obj)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new state"""
    request_obj = request.get_json()
    if request_obj is  None:
        return abort(404, "Not a json")
    if "name" not in request_obj:
        return abort(404, "missing name")

    new_obj = State(**request_obj)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a state object"""
    state_obj = storage.get("State", state_id)
    if not state_obj:
        return abort(404)

    request_obj = request.get_json()
    if request_obj is None:
        return abort(404, "Not a json")
    for k,v in request_obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, k, v)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
