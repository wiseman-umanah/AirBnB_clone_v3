#!/usr/bin/python3
"""Imports from api.vi.views
contains functionality for api"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": Amenity, "cities": City,
    "places": Place, "reviews": Review,
    "states": State, "users": User
    }


@app_views.route('/status')
def status_print():
    """Returns the status OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def retrieve_stats():
    """Retrieves the status of each key"""
    stats = {}
    for key in classes.keys():
        stats[key] = storage.count(classes[key])
    return jsonify(stats)
