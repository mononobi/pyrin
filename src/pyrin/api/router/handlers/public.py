# -*- coding: utf-8 -*-
"""
router handlers public module.
"""

from pyrin.api.router.handlers.base import RouteBase, TemporaryRouteBase


class PublicRoute(RouteBase):
    """
    public route class.

    this class should be used to manage application public api
    routes that do not require authentication.
    """
    pass


class PublicTemporaryRoute(PublicRoute, TemporaryRouteBase):
    """
    public temporary route class.

    this class should be used to manage application public api
    routes that do not require authentication and must be unregistered
    after a specified number of requests or a duration of time.
    this is useful for a couple of different things but mostly for system
    health checking after each new deployment on production.
    """
    pass
