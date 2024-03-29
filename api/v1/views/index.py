#!/usr/bin/python3
"""Imports from api.vi.views
contains functionality for api"""
from api.v1.views import app_views


@app_views.route('/status')
def status_print():
    """Returns the status OK"""
    return {"status": "OK"}
