#!/usr/bin/python3
"""
cities: defining a blueprint view for City object handling all
the default RESTful API actions

    /api/v1/cities/<city_id> [GET, DELETE, PUT]
    /api/v1/states/<state_id>/cities [GET, POST]

"""

from api.v1.views import app_views
from flask import jsonify, request
from flask_restful import Api, Resource, abort
from models import storage
from models.city import City
from models.state import State

api = Api(app_views)


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404, error="Not Found")


class CityRes(Resource):
    """
    This is an API resource for the City object
    for the route: /cities/<city_id>
    """
    def get(self, city_id):
        """Returns an instance of city"""
        result = storage.get(City, city_id)
        error_404(result)
        return result.to_dict()

    def delete(self, city_id):
        """Deletes an instance of city with the specific id"""
        result = storage.get(City, city_id)
        error_404(result)
        storage.delete(result)
        storage.save()
        return {}, 200

    def put(self, city_id):
        """Updates an instance of the city entities"""
        result = storage.get(City, city_id)
        error_404(result)
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        for k, v in args.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(result, k, v)
        result.save()
        return result.to_dict(), 200


class CityStateRes(Resource):
    """
    This is an API resource for the City object
    for the route: /states/<state_id>/cities
    """
    def get(self, state_id):
        """Returns a list of cities with the specific state id"""
        result = storage.get(State, state_id)
        error_404(result)
        return [value.to_dict() for value in result.cities]

    def post(self, state_id):
        """Adds a new instance of City into the dataset"""
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        if not args.get('name'):
            abort(400, message="Missing name")
        result = storage.get(State, state_id)
        error_404(result)
        args['state_id'] = state_id
        new_city = City(**args)
        new_city.save()
        return new_city.to_dict(), 201


api.add_resource(CityStateRes, "/states/<state_id>/cities")
api.add_resource(CityRes, "/cities/<city_id>")
