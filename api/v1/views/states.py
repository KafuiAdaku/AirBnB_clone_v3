#!/usr/bin/python3
"""A module that defines a view functions for the `State` class"""
from models import storage, State
from api.v1.views import app_views
from flask import Flask, jsonify, make_request

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """Retrieves all `State` objects"""


