#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return stats"""
    from models import storage
    from models.state import State
    from models.city import City
    from models.user import User
    from models.place import Place
    from models.review import Review
    from models.amenity import Amenity
    return jsonify({"states": storage.count(State),
                    "cities": storage.count(City),
                    "users": storage.count(User),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "amenities": storage.count(Amenity)})
