#!/usr/bin/python3
"""
amenities: defining a blueprint view for Amenity object handling all
the default RESTful API actions

    /api/v1/amenities [GET, POST]
    /api/v1/amenities/<amenity_id> [DELETE, GET, PUT]
"""

from api.v1.views import app_views
from flask import jsonify, request
from flask_restful import Api, Resource, abort
from models import storage
from models.amenity import Amenity

api = Api(app_views)


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404, error="Not Found")


class AmenityIdRes(Resource):
    """
    This is an API resource for the Amenity object
    for the route: /amenities/<amenity_id>
    """
    def get(self, amenity_id):
        """Returns an instance of amenity"""
        result = storage.get(Amenity, amenity_id)
        error_404(result)
        return result.to_dict()

    def delete(self, amenity_id):
        """Deletes an instance of amenity with the specific id"""
        result = storage.get(Amenity, amenity_id)
        error_404(result)
        storage.delete(result)
        storage.save()
        return {}, 200

    def put(self, amenity_id):
        """Updates an instance of the amenity entities"""
        result = storage.get(Amenity, amenity_id)
        error_404(result)
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        for k, v in args.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(result, k, v)
        result.save()
        return result.to_dict(), 200


class AmenityRes(Resource):
    """
    This is an API resource for the Amenity object
    for the route: /amenities
    """
    def get(self):
        """Returns a list of all amenities"""
        result = storage.all(Amenity)
        error_404(result)
        return [value.to_dict() for value in result.values()]

    def post(self):
        """Adds a new instance of Amenity into the dataset"""
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        if not args.get('name'):
            abort(400, message="Missing name")
        new_amenity = Amenity(**args)
        new_amenity.save()
        return new_amenity.to_dict(), 201


api.add_resource(AmenityIdRes, "/amenities/<amenity_id>")
api.add_resource(AmenityRes, "/amenities")
