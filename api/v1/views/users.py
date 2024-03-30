#!/usr/bin/python3
""" new view for User objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, request, abort


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """get user information for all users"""
    if user_id:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user based on its user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """Transforms HTTP to a dictionary"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    if "email" not in data:
        return jsonify("Missing email"), 400
    if "password" not in data:
        return jsonify("Missing password"), 400
    else:
        new_state = User()
        new_state.email = data["email"]
        new_state.password = data["password"]
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_users(user_id):
    """For updating the database from user"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.name = data["name"]
    storage.save()
    return jsonify(user.to_dict()), 200
