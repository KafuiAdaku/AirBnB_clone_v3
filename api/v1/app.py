#!/usr/bin/python3
"""A module that creates an instance of the flask framework"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(placeholder):
    """closes app context"""
    storage.close()
    return


@app.errorhandler(404)
def page_not_found(exception):
    """Returns a custom 404 response"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", 5000)), threaded=True, debug=True)
