#!/usr/bin/python3
""" module that configures the api status and stats routes"""
from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def api_status():
    """route that returns a JSON status of OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def print_count():
    """method that returns counts of all classes in json format"""
    stats = {}

    cls_names = {
        "states": "State",
        "cities": "City",
        "amenities": "Amenity",
        "places": "Place",
        "reviews": "Review",
        "users": "User",
    }

    for cls_name in cls_names:
        stats[cls_name] = storage.count(cls_names[cls_name])

    return make_response(jsonify(stats))
