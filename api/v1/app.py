#!/usr/bin/python3
"""
Flask web api
"""
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
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
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
