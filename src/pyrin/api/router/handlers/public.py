# -*- coding: utf-8 -*-
"""
router handlers public module.
"""

from pyrin.api.router.handlers.base import RouteBase


class PublicRoute(RouteBase):
    """
    public route class.

    this class should be used to manage application public api
    routes that do not require authentication.
    """
    pass
