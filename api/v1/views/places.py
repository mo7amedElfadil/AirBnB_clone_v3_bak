#!/usr/bin/python3
"""
places: defining a blueprint view for Place object handling all
the default RESTful API actions

    /api/v1/places/<place_id> [GET, DELETE, PUT]
    /api/v1/citys/<city_id>/places [GET, POST]

"""

from api.v1.views import app_views
from flask import jsonify, request
from flask_restful import Api, Resource, abort
from models import storage
from models.city import City
from models.place import Place

api = Api(app_views)


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404, error="Not Found")


class PlaceRes(Resource):
    """
    This is an API resource for the Place object
    for the route: /places/<place_id>
    """
    def get(self, place_id):
        """Returns an instance of place"""
        result = storage.get(Place, place_id)
        error_404(result)
        return result.to_dict()

    def delete(self, place_id):
        """Deletes an instance of place with the specific id"""
        result = storage.get(Place, place_id)
        error_404(result)
        storage.delete(result)
        storage.save()
        return {}, 200

    def put(self, place_id):
        """Updates an instance of the place entities"""
        result = storage.get(Place, place_id)
        error_404(result)
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        for k, v in args.items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(result, k, v)
        result.save()
        return result.to_dict(), 200


class PlaceCityRes(Resource):
    """
    This is an API resource for the Place object
    for the route: /citys/<city_id>/places
    """
    def get(self, city_id):
        """Returns a list of places with the specific city id"""
        result = storage.get(City, city_id)
        error_404(result)
        return [value.to_dict() for value in result.places]

    def post(self, city_id):
        """Adds a new instance of Place into the dataset"""
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        if not args.get('user_id'):
            abort(400, message="Missing user_id")
        if not args.get('name'):
            abort(400, message="Missing name")
        result = storage.get(City, city_id)
        error_404(result)
        args['city_id'] = city_id
        new_place = Place(**args)
        new_place.save()
        return new_place.to_dict(), 201


api.add_resource(PlaceCityRes, "/cities/<city_id>/places")
api.add_resource(PlaceRes, "/places/<place_id>")
