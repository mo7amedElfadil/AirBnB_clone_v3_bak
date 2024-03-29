#!/usr/bin/python3
"""
states: defining a blueprint view for State object handling all
the default RESTful API actions

    /status: returns the status of the API
    /stats: returns the staticstis of the different entities
"""

from api.v1.views import app_views
from flask import jsonify, request
from flask_restful import Api, Resource, abort
from models import storage
from models.state import State

api = Api(app_views)


def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404, error="Not Found")


class StateNoId(Resource):
    """
    This is an API resource for the States object
    for the route: /api/v1/states
    """
    def get(self):
        """Returns a list of states"""
        return [value.to_dict() for value in storage.all(State).values()]

    def post(self):
        """Adds a new instance of State into the dataset"""
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        if not args.get('name'):
            abort(400, message="Missing name")
        new_state = State(**args)
        new_state.save()
        return new_state.to_dict(), 201


class StateApiId(Resource):
    """
    This is an API resource for the States object
    for the route: /api/v1/states/<state_id>
    """
    def get(self, state_id):
        """Returns a state with the specific id"""
        result = storage.get(State, state_id)
        error_404(result)
        return result.to_dict()

    def delete(self, state_id):
        """Deletes an instance of state with the specific id"""
        result = storage.get(State, state_id)
        error_404(result)
        storage.delete(result)
        storage.save()
        return {}, 200

    def put(self, state_id):
        """Updates an instance of the state entities"""
        result = storage.get(State, state_id)
        error_404(result)
        args = request.get_json()
        if not args:
            abort(400, message="Not a JSON")
        for k, v in args.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(result, k, v)
        result.save()
        return result.to_dict(), 200


api.add_resource(StateNoId, "/states")
api.add_resource(StateApiId, "/states/<state_id>")
