#!/usr/bin/python3
"""
users: defining a blueprint view for User object handling all
the default RESTful API actions

    /status: returns the status of the API
    /stats: returns the staticstis of the different entities
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User



def error_404(result):
    """Defining how to process a result that is None"""
    if not result:
        abort(404)


@app_views.route('/users', methods=['GET', 'POST'])
def get_users(self):
    """Returns a list of users"""
    return [value.to_dict() for value in storage.all(User).values()]

def post(self):
    """Adds a new instance of User into the dataset"""
    args = request.get_json()
    if not args:
        abort(400, message="Not a JSON")
    if not args.get('email'):
        abort(400, message="Missing email")
    if not args.get('password'):
        abort(400, message="Missing password")
    new_user = User(**args)
    new_user.save()
    return new_user.to_dict(), 201


def get(self, user_id):
    """Returns a user with the specific id"""
    result = storage.get(User, user_id)
    error_404(result)
    return result.to_dict()

def delete(self, user_id):
    """Deletes an instance of user with the specific id"""
    result = storage.get(User, user_id)
    error_404(result)
    storage.delete(result)
    storage.save()
    return {}, 200

def put(self, user_id):
    """Updates an instance of the user entities"""
    result = storage.get(User, user_id)
    error_404(result)
    args = request.get_json()
    if not args:
        abort(400, message="Not a JSON")
    for k, v in args.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(result, k, v)
    result.save()
    return result.to_dict(), 200



