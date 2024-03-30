#!/usr/bin/python3
""" new view for City objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, request, abort


@app_views.route('/cities/<cities_id>',
                 methods=['GET'], strict_slashes=False)
def get_cities(cities_id=None):
    """get city information for all cities"""
    if cities_id:
        city = storage.get(City, cities_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_state_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.all(State)
    for s in state:
        if state[s].id == state_id:
            stat_city = [city.to_dict() for city in state[s].cities]
            return jsonify(stat_city)
    abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    """deletes a city based on its city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id):
    """Transforms HTTP to a dictionary"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    if "name" not in data:
        return jsonify("Missing name"), 400
    else:
        if storage.get(State, state_id):
            new_city = City()
            new_city.name = data["name"]
            new_city.state_id = state_id
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
        else:
            abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    """For updating the database from user"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.name = data["name"]
    storage.save()
    return jsonify(city.to_dict()), 200
