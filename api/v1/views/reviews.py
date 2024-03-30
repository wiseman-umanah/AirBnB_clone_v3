#!/usr/bin/python3
""" new view for Review objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.state import State
from models import storage
from flask import jsonify, request, abort


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id=None):
    """get review information for all reviews"""
    if review_id:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_place_id(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.all(Place)
    for p in place:
        if place[p].id == place_id:
            pla_rev = [review.to_dict() for review in place[p].reviews]
            return jsonify(pla_rev)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    """deletes a review based on its city_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_reviews(place_id):
    """Transforms HTTP to a dictionary"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    if "user_id" not in data:
        return jsonify("Missing user_id"), 400
    if "text" not in data:
        return jsonify("Missing text"), 400
    else:
        if storage.get(Place, place_id):
            if storage.get(State, data["user_id"]):
                new_review = Review()
                new_review.user_id = data["user_id"]
                new_review.text = data["text"]
                new_review.place_id = place_id
                storage.new(new_review)
                storage.save()
                return jsonify(new_review.to_dict()), 201
            return jsonify({"error": "Place not found"}), 404
        return jsonify({"error": "Place not found"}), 404


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """For updating the database from user"""
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.text = data["text"]
    storage.save()
    return jsonify(review.to_dict()), 200
