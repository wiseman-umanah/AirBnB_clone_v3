#!/usr.bin/python3
""" new view for Place objects that handles
all default RESTFul API actions"""
from models.place import Place
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort, make_response

from os import getenv

status = getenv("HBNB_TYPE_STORAGE")


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def pla_amenity(place_id):
    """get amenity information for a specified place"""
    place = storage.get(Place, place_id)
    if place:
        if status == "db":
            amenity_objs = place.amenities
        else:
            amenity_objs = place.amenity_ids
        amenities = [a.to_dict() for a in amenity_objs]
        return jsonify(amenities)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity object from a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place and amenity:
        if status == "db":
            place_amenities = place.amenities
        else:
            place_amenities = place.amenity_ids
        if amenity not in place_amenities:
            abort(404)
        place_amenities.remove(amenity)
        place.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place and amenity:
        if status == 'db':
            place_amenities = place.amenities
        else:
            place_amenities = place.amenity_ids
        if amenity in place_amenities:
            return jsonify(amenity.to_dict())
        place_amenities.append(amenity)
        place.save()
        return make_response(jsonify(amenity.to_dict()), 201)
    abort(404)
