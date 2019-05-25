# -*- coding: utf-8 -*-
"""
application services module.
"""

from pyrin import _get_app


def add_context(key, value, **options):
    """
    adds the given key and it's value into the application context.

    :param str key: related key for storing application context.
    :param object value: related value for storing in application context.

    :keyword bool replace: specifies that if there is already a value with
                           the same key in application context, it should be updated
                           with new value, otherwise raise an error. defaults to False.

    :raises DuplicateContextKeyError: duplicate context key error.
    """

    _get_app().add_context(key, value, **options)


def get_context(key):
    """
    gets the application context value that belongs to given key.

    :param str key: key for requested application context.

    :rtype: object
    """

    return _get_app().get_context(key)


def register_component(component, **options):
    """
    registers given application component or replaces the existing one
    if `replace=True` is provided. otherwise, it raises an error
    on adding an instance which it's id is already available
    in registered components.

    :param Component component: component instance.

    :keyword bool replace: specifies that if there is another registered
                           component with the same id, replace it with the new one.
                           otherwise raise an error. defaults to False.

    :raises InvalidComponentTypeError: invalid component type error.
    :raises InvalidComponentIDError: invalid component id error.
    :raises DuplicateComponentIDError: duplicate component id error.
    """

    _get_app().register_component(component, **options)


def get_component(component_id, **options):
    """
    gets the specified application component.

    :param str component_id: component unique id.

    :keyword object __custom_key__: custom key of component to get.

    :rtype: Component
    """

    return _get_app().get_component(component_id, **options)


def register_error_handler(code_or_exception, func):
    """
    registers the given function as an error handler for given code or exception type.

    :param Union[int, Exception] code_or_exception: code or exception to
                                                    register error handler for.

    :param callable func: function to register it as an error handler.
    """

    _get_app().register_error_handler(code_or_exception, func)


def register_before_request_handler(func):
    """
    registers the given function into application before request handlers.

    :param callable func: function to register it into before request handlers.
    """

    _get_app().before_request(func)


def register_after_request_handler(func):
    """
    registers the given function into application after request handlers.

    :param callable func: function to register it into after request handlers.
    """

    _get_app().after_request(func)


def add_url_rule(rule, endpoint=None, view_func=None,
                 provide_automatic_options=None, **options):
    """
    connects a url rule. if a view_func is provided it will be registered with the endpoint.
    if there is another rule with the same url and `replace=True` option is provided,
    it will be replaced, otherwise an error will be raised.

    :param str rule: the url rule as string.

    :param str endpoint: the endpoint for the registered url rule.
                         pyrin itself assumes the url rule as endpoint.

    :param callable view_func: the function to call when serving a request to the
                               provided endpoint.

    :param bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                           added automatically.
                                           this can also be controlled by setting the
                                           `view_func.provide_automatic_options = False`
                                           before adding the rule.

    :keyword tuple(str) methods: http methods that this rule should handle.
                                 if not provided, defaults to `GET`.

    :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                to access this route's resource.

    :keyword bool login_required: specifies that this route could not be accessed
                                  if the requester has not a valid token.
                                  defaults to True if not provided.

    :keyword bool replace: specifies that this route must replace
                           any existing route with the same url or raise
                           an error if not provided. defaults to False.

    :raises DuplicateRouteURLError: duplicate route url error.
    """

    _get_app().add_url_rule(rule, endpoint, view_func,
                            provide_automatic_options, **options)


def register_route_factory(factory):
    """
    registers a route factory as application url rule class.

    :param callable factory: route factory.
                             it could be a class or a factory method.

    :raises InvalidRouteFactoryTypeError: invalid route factory type error.
    """

    _get_app().register_route_factory(factory)


def get_settings_path():
    """
    gets the application settings path.

    :rtype: str
    """

    return _get_app().get_settings_path()
