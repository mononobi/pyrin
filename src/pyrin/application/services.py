# -*- coding: utf-8 -*-
"""
application services module.
"""

from pyrin.application.container import _get_app


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

    get_current_app().add_context(key, value, **options)


def get_context(key):
    """
    gets the application context value that belongs to given key.

    :param str key: key for requested application context.

    :returns: related value to given key.
    """

    return get_current_app().get_context(key)


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

    get_current_app().register_component(component, **options)


def remove_component(component_id):
    """
    removes application component with given id.

    :param tuple component_id: component id to be removed.
    :type component_id: tuple(str, object)

    :raises ComponentAttributeError: component attribute error.
    """

    get_current_app().remove_component(component_id)


def get_component(component_name, **options):
    """
    gets the specified application component.

    :param str component_name: component name.

    :keyword object component_custom_key: component custom key.
                                          if not provided, tries to get it from
                                          request object, if not found,
                                          `DEFAULT_COMPONENT_KEY` will be used.

    :rtype: Component
    """

    return get_current_app().get_component(component_name, **options)


def register_error_handler(code_or_exception, func):
    """
    registers the given function as an error handler for given code or exception type.

    :param Union[int, Exception] code_or_exception: code or exception to
                                                    register error handler for.

    :param callable func: function to register it as an error handler.
    """

    get_current_app().register_error_handler(code_or_exception, func)


def register_before_request_handler(func):
    """
    registers the given function into application before request handlers.

    :param callable func: function to register it into before request handlers.
    """

    get_current_app().before_request(func)


def register_after_request_handler(func):
    """
    registers the given function into application after request handlers.

    :param callable func: function to register it into after request handlers.
    """

    get_current_app().after_request(func)


def register_teardown_request_handler(func):
    """
    registers the given function into application teardown request handlers.
    teardown request handlers should not return any value
    and also should not raise any exception.

    :param callable func: function to register it into teardown request handlers.
    """

    get_current_app().teardown_request(func)


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

    get_current_app().add_url_rule(rule, endpoint, view_func,
                                   provide_automatic_options, **options)


def register_route_factory(factory):
    """
    registers a route factory as application url rule class.

    :param callable factory: route factory.
                             it could be a class or a factory method.

    :raises InvalidRouteFactoryTypeError: invalid route factory type error.
    """

    get_current_app().register_route_factory(factory)


def get_current_route_factory():
    """
    gets current route factory in use.

    :rtype: callable
    """

    return get_current_app().get_current_route_factory()


def get_settings_path():
    """
    gets the application settings path.

    :rtype: str
    """

    return get_current_app().get_settings_path()


def get_migrations_path():
    """
    gets the application migrations path.

    :rtype: str
    """

    return get_current_app().get_migrations_path()


def get_locale_path():
    """
    gets the application locale path.

    :rtype: str
    """

    return get_current_app().get_locale_path()


def get_application_main_package_path():
    """
    gets the application main package path.

    :rtype: str
    """

    return get_current_app().get_application_main_package_path()


def get_pyrin_root_path():
    """
    gets pyrin root path in which pyrin package is located.

    :rtype: str
    """

    return get_current_app().get_pyrin_root_path()


def get_application_root_path():
    """
    gets the application root path in which application package is located.

    :rtype: str
    """

    return get_current_app().get_application_root_path()


def get_pyrin_main_package_path():
    """
    gets pyrin main package path.

    :rtype: str
    """

    return get_current_app().get_pyrin_main_package_path()


def get_configs():
    """
    gets a shallow copy of application's configuration dictionary.

    :rtype: dict
    """

    return get_current_app().get_configs()


def configure(config_store):
    """
    configures the application with given dict.
    all keys will be converted to uppercase for flask compatibility.

    :param dict config_store: a dictionary containing configuration key/values.
    """

    get_current_app().configure(config_store)


def get_current_app():
    """
    gets the instance of current running application.

    :rtype: Application
    """

    return _get_app()


def register_hook(instance):
    """
    registers the given instance into application hooks.

    :param ApplicationHookBase instance: application hook instance to be registered.

    :raises InvalidApplicationHookTypeError: invalid application hook type error.
    """

    get_current_app().register_hook(instance)


def is_scripting_mode():
    """
    gets a value indicating that application has been started in scripting mode.
    some application hooks will not fire in this mode. like 'before_application_start'.
    """

    return get_current_app().is_scripting_mode()


def get_application_name():
    """
    gets the application name.

    :rtype: str
    """

    return get_current_app().get_application_name()
