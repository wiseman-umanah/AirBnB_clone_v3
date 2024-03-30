#!/usr/bin/python3
""" new view for State objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """get state information for all states"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state based on its state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """Transforms HTTP to a dictionary"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    if "name" not in data:
        return jsonify("Missing name"), 400
    else:
        new_state = State()
        new_state.name = data["name"]
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """For updating the database from user"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.name = data["name"]
    storage.save()
    return jsonify(state.to_dict()), 200
