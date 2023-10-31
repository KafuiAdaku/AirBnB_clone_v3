#!/usr/bin/python3
"""Index module"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage

@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    stats = {}
    classes = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User",
            }
    for cls in classes:
        stats[cls] = storage.count(classes[cls])
    return make_response(jsonify(stats))
