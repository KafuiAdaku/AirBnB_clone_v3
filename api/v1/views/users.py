#!/usr/bin/python3
"""View functions for `User` objects"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request

@app_views.route("/users", methods=["GET"], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieves all `User` objects"""
    if not user_id:
        users = storage.all("User")
        list_users = [user.to_dict for user in users]
        return jsonify(list_users)

    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a new `User` obect"""
    request_obj = request.get_json()
    if request_obj is None:
        abort(400, "Not a JSON")
    if "email" not in request_obj:
        abort(400, "Missing email")
    if "password" not in request_obj:
        abort(400, "Missing password")
    user = User(**request_obj)
    user.save()
    return make_response(jsonify(user.to_dict), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a `User` object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    request_obj = request.get_json()
    if request_obj is None:
        abort(404, "Not a JSON")

    for k,v in request_obj:
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
