#!/usr/bin/python3
""" new view for Amenity objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, request, abort


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """get amenity information for all amenities"""
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a amenity based on its amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Transforms HTTP to a dictionary"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    if "name" not in data:
        return jsonify("Missing name"), 400
    else:
        new_state = Amenity()
        new_state.name = data["name"]
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """For updating the database from user"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.name = data["name"]
    storage.save()
    return jsonify(amenity.to_dict()), 200
