# -*- coding: utf-8 -*-
"""
router services module.
"""

from pyrin.api.router.component import RouterComponent
from pyrin.application.decorators import route_factory
from pyrin.application.services import get_component


@route_factory()
def create_route(instance, rule, **options):
    """
    creates the appropriate route based on the input parameters.

    :param Application instance: caller object instance, it should be an application instance.
                                 this value will not used. it just added for compatibility
                                 with flask.

    :param str rule: unique url rule to register this route for.
                     routes with duplicated urls will be overwritten
                     if `replace=True` option is provided, otherwise an error
                     will be raised.

    :keyword list[str] methods: http methods that this route could handle.
                                if not provided, defaults to `GET`, `HEAD`
                                and `OPTIONS`.

    :keyword callable view_func: a function to be called on accessing this route.

    :keyword str endpoint: the endpoint for the registered url rule. flask
                           itself assumes the name of the view function as
                           endpoint if not provided.

    :keyword bool login_required: specifies that this route could not be accessed
                                  if the requester has not a valid token.
                                  defaults to True if not provided.

    :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                to access this route's resource.

    :rtype: RouteBase
    """

    return get_component(RouterComponent.COMPONENT_ID).create_route(rule, **options)
