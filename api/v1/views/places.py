#!/usr/bin/python3
""" new view for Place objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, request, abort


@app_views.route('/places/<places_id>', methods=['GET'], strict_slashes=False)
def get_places(places_id=None):
    """get place information for all places"""
    if places_id:
        place = storage.get(Place, places_id)
        if place is None:
            return jsonify({"error": "Place not found"}), 404
        return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_city_id(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.all(City)
    for c in city:
        if city[c].id == city_id:
            cit_place = [place.to_dict() for place in city[c].places]
            return jsonify(cit_place)
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """deletes a place based on its city_id"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Place not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """Transforms HTTP to a dictionary"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    if "user_id" not in data:
        return jsonify("Missing user_id"), 400
    if "name" not in data:
        return jsonify("Missing name"), 400
    else:
        if storage.get(City, city_id) and storage.get(State, data["user_id"]):
            new_place = Place()
            new_place.user_id = data["user_id"]
            new_place.name = data["name"]
            new_place.city_id = city_id
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_places(place_id):
    """For updating the database from user"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.name = data["name"]
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches for a place"""
    data = request.get_json()
    if data is not None:
        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return jsonify({'error': 'Not a JSON'}), 400
