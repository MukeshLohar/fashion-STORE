"""
Context processors for the shop app

This module contains context processors that make data available
to all templates throughout the application.
"""

from .cart import Cart


def cart(request):
    """Make cart available in all templates"""
    return {'cart': Cart(request)}