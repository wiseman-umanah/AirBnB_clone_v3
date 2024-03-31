#!/usr/bin/python3
"""Starts a Flask web project
with rooting functionalities and Blueprints"""
from flask import Flask
from models import storage
from flask import jsonify
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv

host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else "5000"

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """For closing sessions of database"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by returning a custom JSON response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
