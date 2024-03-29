#!/usr/bin/python3
"""Creates the Blueprint for separate routing
Routes located at ...index"""
from flask import Blueprint


app_views = Blueprint("app_view", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
