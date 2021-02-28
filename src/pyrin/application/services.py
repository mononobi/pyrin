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


def get_context(key, **options):
    """
    gets the application context value that belongs to given key.

    :param str key: key for requested application context.

    :keyword object default: default value to be returned if key is not available.
                             otherwise, it raises an error if key is not available.

    :raises ContextAttributeError: context attribute error.

    :returns: related value to given key.
    """

    return get_current_app().get_context(key, **options)


def register_component(component, **options):
    """
    registers given application component or replaces the existing one.

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

    :param tuple[str, object] component_id: component id to be removed.

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

    :raises InvalidComponentNameError: invalid component name error.
    :raises ComponentAttributeError: component attribute error.

    :rtype: Component
    """

    return get_current_app().get_component(component_name, **options)


def register_error_handler(code_or_exception, func):
    """
    registers the given function as an error handler for given code or exception type.

    :param int | type[Exception] code_or_exception: code or exception to
                                                    register error handler for.

    :param function func: function to register it as an error handler.
    """

    get_current_app().register_error_handler(code_or_exception, func)


def register_before_request_handler(func):
    """
    registers the given function into application before request handlers.

    :param function func: function to register it into before request handlers.
    """

    get_current_app().before_request(func)


def register_after_request_handler(func):
    """
    registers the given function into application after request handlers.

    :param function func: function to register it into after request handlers.
    """

    get_current_app().after_request(func)


def register_teardown_request_handler(func):
    """
    registers the given function into application teardown request handlers.

    teardown request handlers should not return any value
    and also should not raise any exception.

    :param function func: function to register it into teardown request handlers.
    """

    get_current_app().teardown_request(func)


def add_url_rule(rule, view_func,
                 provide_automatic_options=None, **options):
    """
    connects a url rule. the provided view_func will be registered with the endpoint.

    if there is another rule with the same url and http methods and `replace=True`
    option is provided, it will be replaced. otherwise an error will be raised.

    a note about endpoint. pyrin will handle endpoint generation on its own.
    so there is no endpoint parameter in this method's signature.
    this is required to be able to handle uniqueness of endpoints and managing them.
    despite flask, pyrin will not require you to define view functions with unique names.
    you could define view functions with the same name in different modules. but to
    ensure the uniqueness of endpoints, pyrin will use the fully qualified name
    of function as endpoint. for example: `pyrin.api.services.create_route`.
    so you could figure out endpoint for any view function to use it in places
    like `url_for` method.

    pyrin handles endpoints this way to achieve these two important features:

    1. dismissal of the need for view function name uniqueness.
       when application grows, it's nonsense to be forced to have
       unique view function names at application level.

    2. managing routes with the same url and http methods, and informing
       the developer about them to prevent accidental replacements. and also
       providing a way to replace a route by another route with the same url
       and http methods if that is what developer actually wants.
       when application grows, it becomes a point of failure when you have no
       idea that you've registered a similar route in multiple places and only
       one of them will be get called based on registration order.

    :param str rule: the url rule as string.

    :param function view_func: the function to call when serving a request to the
                               provided endpoint.

    :param bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                           added automatically.
                                           this can also be controlled by setting the
                                           `view_func.provide_automatic_options = False`
                                           before adding the rule.

    :keyword str | tuple[str] methods: http methods that this rule should handle.
                                       if not provided, defaults to `GET`.

    :keyword PermissionBase | tuple[PermissionBase] permissions: all required permissions
                                                                 for accessing this route.

    :keyword bool authenticated: specifies that this route could not be accessed
                                 if the requester has not been authenticated.
                                 defaults to True if not provided.

    :keyword bool fresh_auth: specifies that this route could not be accessed
                              if the requester has not a fresh authentication.
                              fresh authentication means an authentication that
                              has been done by providing user credentials to
                              server. defaults to False if not provided.

    :keyword bool replace: specifies that this route must replace any existing
                           route with the same url and http methods or raise
                           an error if not provided. defaults to False.

    :keyword dict defaults: an optional dict with defaults for other rules with the
                            same endpoint. this is a bit tricky but useful if you
                            want to have unique urls.

    :keyword str subdomain: the subdomain rule string for this rule. If not specified the
                            rule only matches for the `default_subdomain` of the map. if
                            the map is not bound to a subdomain this feature is disabled.

    :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only for
                                  this rule. if not specified the `Map` setting is used.

    :keyword bool merge_slashes: override `Map.merge_slashes` for this rule.

    :keyword bool build_only: set this to True and the rule will never match but will
                              create a url that can be build. this is useful if you have
                              resources on a subdomain or folder that are not handled by
                              the WSGI application (like static data)

    :keyword str | callable redirect_to: if given this must be either a string
                                         or callable. in case of a callable it's
                                         called with the url adapter that
                                         triggered the match and the values
                                         of the url as keyword arguments and has
                                         to return the target for the redirect,
                                         otherwise it has to be a string with
                                         placeholders in rule syntax.

    :keyword bool alias: if enabled this rule serves as an alias for another rule with
                         the same endpoint and arguments.

    :keyword str host: if provided and the url map has host matching enabled this can be
                       used to provide a match rule for the whole host. this also means
                       that the subdomain feature is disabled.

    :keyword bool websocket: if set to True, this rule is only matches for
                             websocket (`ws://`, `wss://`) requests. by default,
                             rules will only match for http requests.
                             defaults to False if not provided.

    :keyword int max_content_length: max content length that this route could handle,
                                     in bytes. if not provided, it will be set to
                                     `restricted_max_content_length` api config key.
                                     note that this value should be lesser than or equal
                                     to `max_content_length` api config key, otherwise
                                     it will cause an error.

    :keyword int status_code: status code to be returned on successful responses.
                              defaults to corresponding status code of request's
                              http method if not provided.

    :note status_code: it could be a value from `InformationResponseCodeEnum`
                       or `SuccessfulResponseCodeEnum` or `RedirectionResponseCodeEnum`.

    :keyword bool strict_status: specifies that it should only consider
                                 the status code as processed if it is from
                                 `InformationResponseCodeEnum` or
                                 `SuccessfulResponseCodeEnum` or
                                 `RedirectionResponseCodeEnum` values. otherwise
                                 all codes from `INFORMATION_CODE_MIN`
                                 to `INFORMATION_CODE_MAX` or from
                                 `SUCCESS_CODE_MIN` to `SUCCESS_CODE_MAX`
                                 or from `REDIRECTION_CODE_MIN` to
                                 `REDIRECTION_CODE_MAX` will be considered
                                 as processed. defaults to True if not provided.

    :keyword str | list[str] environments: a list of all environments that this
                                           route must be exposed on them.
                                           the values could be from all available
                                           environments in environments config store.
                                           for example: `production`, `development`.
                                           if not provided, the route will be exposed
                                           on all environments.

    :keyword ResultSchema | type[ResultSchema] result_schema: result schema to be used
                                                              to filter results. it could
                                                              be an instance or a type
                                                              of `ResultSchema` class.

    :keyword bool indexed: specifies that list results must
                           include an extra field as row index.
                           the name of the index field and the initial value
                           of index could be provided by `index_name` and
                           `start_index` respectively. `indexed` keyword has
                           only effect if the returning result contains a list
                           of objects.

    :keyword str index_name: name of the extra field to contain
                             the row index of each result. if not provided
                             defaults to `row_num` value.

    :keyword int start_index: the initial value of row index. if not
                              provided, starts from 1.

    :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute which
                                                  has `allow_read=False` or its name starts with
                                                  underscore `_`, should not be included in
                                                  result dict. defaults to `SECURE_TRUE` if
                                                  not provided. it will be used only for
                                                  entity conversion. this value will override
                                                  the corresponding value of `result_schema`
                                                  if provided.

    :keyword int depth: a value indicating the depth for conversion.
                        for example if entity A has a relationship with
                        entity B and there is a list of B in A, if `depth=0`
                        is provided, then just columns of A will be available
                        in result dict, but if `depth=1` is provided, then all
                        B entities in A will also be included in the result dict.
                        actually, `depth` specifies that relationships in an
                        entity should be followed by how much depth.
                        note that, if `columns` is also provided, it is required to
                        specify relationship property names in provided columns.
                        otherwise they won't be included even if `depth` is provided.
                        defaults to `default_depth` value of database config store.
                        please be careful on increasing `depth`, it could fail
                        application if set to higher values. choose it wisely.
                        normally the maximum acceptable `depth` would be 2 or 3.
                        there is a hard limit for max valid `depth` which is set
                        in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                        `depth` value than this limit, will cause an error.
                        it will be used only for entity conversion.
                        this value will override the corresponding value of
                        `result_schema` if provided.

    :keyword bool no_cache: a value indicating that the response returning from this route
                            must have a `Cache-Control: no-cache` header. this header will
                            be automatically added. defaults to False if not provided.

    :keyword int request_limit: number of allowed requests to this
                                route before it unregisters itself.
                                defaults to None if not Provided.

    :keyword int lifetime: number of seconds in which this route must remain
                           responsive after initial registration. after this
                           period, the route will unregister itself.
                           defaults to None if not provided.

    :note request_limit, lifetime: if both of these values are provided, this
                                   route will unregister itself if any of
                                   these two conditions are met.

    :keyword bool paged: specifies that this route should return paginated results.
                         defaults to False if not provided.

    :keyword int page_size: default page size for this route.
                            defaults to `default_page_size` from
                            `database` config store if not provided.

    :keyword int max_page_size: maximum page size that client is allowed
                                to request for this route. defaults to
                                `max_page_size` from `database` configs store
                                if not provided.

    :keyword bool cors_enabled: specifies that cross origin resource sharing is enabled.
                                if not provided, it will be get from cors config store.

    :keyword bool cors_always_send: specifies that cors headers must be included in
                                    response even if the request does not have origin header.
                                    if not provided, it will be get from cors config store.

    :keyword list[str] cors_allowed_origins: a list of extra allowed origins to be used
                                             in conjunction with default allowed ones.

    :keyword list[str] cors_exposed_headers: extra exposed headers to be combined
                                             with default ones.

    :keyword list[str] cors_allowed_headers: extra allowed headers to be combined
                                             with default ones.

    :keyword bool cors_allow_credentials: specifies that browsers are allowed to pass
                                          response headers to front-end javascript code
                                          if the route is authenticated.
                                          if not provided, it will be get from cors config
                                          store.

    :keyword int cors_max_age: maximum number of seconds to cache results.
                               if not provided, it will be get from cors config store.

    :raises DuplicateRouteURLError: duplicate route url error.
    :raises OverwritingEndpointIsNotAllowedError: overwriting endpoint is not allowed error.
    :raises PageSizeLimitError: page size limit error.
    :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
    :raises InvalidViewFunctionTypeError: invalid view function type error.
    :raises InvalidResultSchemaTypeError: invalid result schema type error.
    :raises InvalidResponseStatusCodeError: invalid response status code error.
    """

    get_current_app().add_url_rule(rule, view_func, provide_automatic_options, **options)


def generate_endpoint(func, **options):
    """
    generates endpoint for given function.

    pyrin will assume endpoint as function's fully qualified name.
    this method could be overridden in subclasses to change the endpoint generation.

    :param function func: function to generate endpoint for it.

    :rtype: str
    """

    return get_current_app().generate_endpoint(func, **options)


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


def get_default_settings_path():
    """
    gets the pyrin default settings path.

    :rtype: str
    """

    return get_current_app().get_default_settings_path()


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


def get_working_directory():
    """
    gets working directory path of application.

    working directory is where the root application and test package are resided.
    this is required when application starts from any of test applications.
    then we should move root path up, to the correct root to be able to
    include real application packages too.
    if the application has been started from real application, this method
    returns the same result as `get_application_root_path()` method.

    :rtype: str
    """

    return get_current_app().get_working_directory()


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


def load_configs(**options):
    """
    loads all configurations related to application package.

    normally, you should not call this method manually.
    """

    get_current_app().load_configs(**options)


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

    some application hooks will not fire in this mode. like 'before_application_run'.
    """

    return get_current_app().is_scripting_mode()


def get_application_name():
    """
    gets the application name.

    it is actually the application main package name.
    first, it gets the import name of application if available.
    otherwise gets the first part of application package name

    :rtype: str
    """

    return get_current_app().get_application_name()


def get_class_name():
    """
    gets the application class name.

    it is required for template generation.

    :rtype: str
    """

    return get_current_app().get_class_name()


def get_module_name():
    """
    gets the application module name.

    it is required for template generation.

    :rtype: str
    """

    return get_current_app().get_module_name()


def get_application_version():
    """
    gets application version.

    :rtype: str
    """

    return get_current_app().get_application_version()


def get_pyrin_version():
    """
    gets pyrin version.

    :rtype: str
    """

    return get_current_app().get_pyrin_version()


def got_first_request():
    """
    gets a value indicating that application has been served at least one request.

    :rtype: bool
    """

    return get_current_app().got_first_request


def get_current_url_adapter():
    """
    gets url adapter of current request.

    if request context is not present, this method raises an error.

    :rtype: MapAdapter
    """

    return get_current_app().get_current_url_adapter()
