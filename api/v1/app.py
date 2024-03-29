#!/usr/bin/python3
"""
Flask web api
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(_=None):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", 5000),
            threaded=True)
