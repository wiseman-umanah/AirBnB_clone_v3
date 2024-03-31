#!/usr/bin/python3
"""Testing documentation of a module
"""
from importlib import import_module
import sys

m_imported = import_module("api.v1.views.places_reviews")

if m_imported.__doc__ is None:
    print("No module documentation", end="")
else:
    print("OK", end="")